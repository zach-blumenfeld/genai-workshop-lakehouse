"""SOLUTION: Open recalls this vehicle is in scope for but never received.

Federated, domain-agnostic: the recall documents and their remedy parts come
from the Neo4j document graph (full-text grounding - no RecallNotice/Part entity
nodes); the vehicle's model, the supersession check, and the repair history come
from live BigQuery rows.

Usage: python solutions/scripts/recall_exposure.py <VIN>
"""

import json
import sys

from db import query
from bq import bq_query, table

vin = sys.argv[1]

# BigQuery: the vehicle's model (rows live here, not in the graph).
veh = bq_query(f"SELECT model FROM {table('vehicles')} WHERE vin = @vin", {"vin": vin})
if not veh:
    print("[]")
    sys.exit()
model = veh[0]["model"]

# Neo4j: recall-notice sections that name this model (full-text, scoped to the
# recalls folder). Read the remedy part numbers from the recall prose.
NEO = """
CALL db.index.fulltext.queryNodes('content_search', $model) YIELD node, score
WHERE node:Section AND node.uri STARTS WITH 'technical-library/recalls/'
MATCH (doc:Document)-[:HAS*]->(node)
RETURN doc.id AS recall, doc.title AS title, node.uri AS uri, node.content AS content
"""
sections = query(NEO, model=model)
if not sections:
    print("[]")
    sys.exit()

all_parts = [p["part_number"] for p in bq_query(f"SELECT part_number FROM {table('parts')}")]

# Per recall: the parts its sections mention, with grounding section URIs.
recalls = {}
for s in sections:
    r = recalls.setdefault(s["recall"], {"recall": s["recall"], "title": s["title"],
                                         "parts": set(), "grounding": set()})
    found = [pn for pn in all_parts if pn in (s["content"] or "")]
    if found:
        r["parts"].update(found)
        r["grounding"].add(s["uri"])

# Candidate remedies: (recall, part) pairs.
candidates = [{"recall": r["recall"], "title": r["title"], "remedyPart": pn,
               "grounding": sorted(r["grounding"])}
              for r in recalls.values() for pn in r["parts"]]
if not candidates:
    print("[]")
    sys.exit()
parts = list({c["remedyPart"] for c in candidates})

# BigQuery: drop parts that are superseded (not the current remedy) and parts
# this vehicle has already received.
superseded = {r["part_number"] for r in bq_query(
    f"SELECT part_number FROM {table('parts')} "
    "WHERE part_number IN UNNEST(@parts) AND superseded_by IS NOT NULL AND superseded_by != ''",
    {"parts": parts})}
applied = {r["part_number"] for r in bq_query(
    f"SELECT DISTINCT wop.part_number FROM {table('work_orders')} wo "
    f"JOIN {table('work_order_parts')} wop ON wop.wo_id = wo.wo_id "
    "WHERE wo.vin = @vin AND wop.part_number IN UNNEST(@parts)", {"vin": vin, "parts": parts})}

# Exposure: a current (non-superseded) remedy this vehicle never received.
exposed = [c for c in candidates
           if c["remedyPart"] not in superseded and c["remedyPart"] not in applied]
print(json.dumps(exposed, indent=2, default=str))
