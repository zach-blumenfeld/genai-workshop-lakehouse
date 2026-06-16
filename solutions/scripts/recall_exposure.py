"""SOLUTION: Open recalls this vehicle is in scope for but never received.

Federated: the recall and its remedy part come from the Neo4j document graph;
the vehicle's model, the supersession check, and the repair history come from
live BigQuery rows.

Usage: python solutions/scripts/recall_exposure.py CM-FAL-2020-0451
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

# Neo4j: recalls for this model, and every part their sections reference.
NEO = """
MATCH (r:RecallNotice {model: $model})-[:HAS*]->(sec:Section)-[:REFERENCES_PART]->(remedy:Part)
RETURN r.id AS recall, r.title AS title, remedy.partNumber AS remedyPart,
       collect(DISTINCT sec.uri) AS grounding
"""
candidates = query(NEO, model=model)
if not candidates:
    print("[]")
    sys.exit()
parts = list({c["remedyPart"] for c in candidates})

# BigQuery: which of those parts are superseded (not a current remedy), and
# which this vehicle has already received.
superseded = {r["part_number"] for r in bq_query(
    f"SELECT part_number FROM {table('parts')} "
    "WHERE part_number IN UNNEST(@parts) AND superseded_by IS NOT NULL", {"parts": parts})}
applied = {r["part_number"] for r in bq_query(
    f"SELECT DISTINCT wop.part_number FROM {table('work_orders')} wo "
    f"JOIN {table('work_order_parts')} wop ON wop.wo_id = wo.wo_id "
    "WHERE wo.vin = @vin AND wop.part_number IN UNNEST(@parts)", {"vin": vin, "parts": parts})}

# Exposure: a current (non-superseded) remedy this vehicle never received.
exposed = [c for c in candidates
           if c["remedyPart"] not in superseded and c["remedyPart"] not in applied]
print(json.dumps(exposed, indent=2, default=str))
