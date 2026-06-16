"""SOLUTION: Evidence-ranked fixes for a code on vehicles like this one.

Federated: the document grounding comes from Neo4j, the repair outcomes come
from live BigQuery SQL, and the two are joined here.

Usage: python solutions/scripts/what_fixed_this.py CM-FAL-2020-0451 P0301
"""

import json
import sys

from db import query
from bq import bq_query, table

vin, code = sys.argv[1], sys.argv[2]

# Step 1 - Neo4j: documents that cover the code, and the parts they reference.
# These are the candidate fixes, each with its guidance and grounding sections.
NEO = """
MATCH (doc:Document)-[:HAS*]->(:Section)-[:REFERENCES_CODE]->(:DTC {code: $code})
MATCH (doc)-[:HAS*]->(gs:Section)-[:REFERENCES_PART]->(part:Part)
RETURN part.partNumber AS partNumber, part.name AS name,
       collect(DISTINCT doc.title) AS guidance,
       collect(DISTINCT gs.uri) AS grounding
"""
candidates = {r["partNumber"]: r for r in query(NEO, code=code)}
if not candidates:
    print("[]")
    sys.exit()

# Step 2 - BigQuery: the vehicle's model/engine, then real outcomes for those
# parts on similar vehicles with the same code (live rows, never migrated).
veh = bq_query(f"SELECT model, engine FROM {table('vehicles')} WHERE vin = @vin", {"vin": vin})
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
