"""SOLUTION: Evidence-ranked fixes for a code on vehicles like this one.

Federated, and domain-agnostic: the document graph has no Part/DTC entity nodes.
Grounding comes from full-text search over the document sections (the code is a
token in the prose); candidate parts are read from those grounding sections'
text and matched against the live parts catalog; the repair outcomes come from
live BigQuery SQL. The two are joined here.

Usage: python solutions/scripts/what_fixed_this.py <VIN> <CODE>
"""

import json
import sys

from db import query
from bq import bq_query, table

vin, code = sys.argv[1], sys.argv[2]

# Step 1 - Neo4j: sections that mention the code (full-text), with their owning
# document title and full text. No entity traversal - the code is just a token.
NEO = """
CALL db.index.fulltext.queryNodes('content_search', $code) YIELD node, score
WHERE node:Section
MATCH (doc:Document)-[:HAS*]->(node)
RETURN node.uri AS uri, node.content AS content, doc.title AS guidance
ORDER BY score DESC LIMIT 25
"""
sections = query(NEO, code=code)
if not sections:
    print("[]")
    sys.exit()

# Candidate parts = parts whose number appears in the grounding text. The parts
# catalog lives in BigQuery (never migrated); read the section prose for them.
all_parts = bq_query(f"SELECT part_number, name FROM {table('parts')}")
candidates = {}
for p in all_parts:
    pn = p["part_number"]
    hits = [s for s in sections if pn in (s["content"] or "")]
    if hits:
        candidates[pn] = {
            "partNumber": pn, "name": p["name"],
            "guidance": sorted({s["guidance"] for s in hits}),
            "grounding": [s["uri"] for s in hits],
        }
if not candidates:
    print("[]")
    sys.exit()

# Step 2 - BigQuery: the vin's model/engine, then real outcomes for those
# candidate parts on similar vehicles with the same code (live rows).
veh = bq_query(f"SELECT model, engine FROM {table('vehicles')} WHERE vin = @vin", {"vin": vin})
if not veh:
    print("[]")
    sys.exit()
model, engine = veh[0]["model"], veh[0]["engine"]

SQL = f"""
SELECT wop.part_number AS partNumber,
       ANY_VALUE(pt.name) AS name,
       COUNT(DISTINCT wo.wo_id) AS timesUsed,
       COUNTIF(wo.comeback) AS comebacks
FROM {table('work_orders')} wo
JOIN {table('vehicles')} v ON wo.vin = v.vin
JOIN {table('work_order_parts')} wop ON wop.wo_id = wo.wo_id
JOIN {table('parts')} pt ON pt.part_number = wop.part_number
WHERE v.model = @model AND v.engine = @engine AND wo.dtc_code = @code
  AND wop.part_number IN UNNEST(@candidates)
GROUP BY wop.part_number
"""
outcomes = bq_query(
    SQL, {"model": model, "engine": engine, "code": code, "candidates": list(candidates)})

# Step 3 - join + rank. Only parts with real repair evidence are answers
# ("what FIXED this", not "what a doc happened to mention"); evidence beats
# guidance, zero comebacks wins. No evidence -> empty -> the agent escalates.
rows = []
for o in outcomes:
    c = candidates[o["partNumber"]]
    rows.append({
        "partNumber": o["partNumber"], "name": o["name"], "guidance": c["guidance"],
        "timesUsed": int(o["timesUsed"]), "comebacks": int(o["comebacks"]),
        "grounding": c["grounding"],
    })
rows.sort(key=lambda r: (r["comebacks"], -r["timesUsed"]))
print(json.dumps(rows, indent=2, default=str))
