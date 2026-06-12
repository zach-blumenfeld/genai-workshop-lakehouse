"""SOLUTION: Evidence-ranked fixes for a code on vehicles like this one.

Usage: python solutions/scripts/what_fixed_this.py CM-FAL-2020-0451 P0301
"""

import json
import sys

from db import query

vin, code = sys.argv[1], sys.argv[2]

CYPHER = """
MATCH (v:Vehicle {vin: $vin}), (c:DTC {code: $code})
MATCH (doc:Document)-[:HAS*]->(:Section)-[:REFERENCES_CODE]->(c)
MATCH (doc)-[:HAS*]->(:Section)-[:REFERENCES_PART]->(part:Part)
MATCH (other:Vehicle {model: v.model, engine: v.engine})
      -[:HAS_WORK_ORDER]->(wo:WorkOrder)-[:DIAGNOSED]->(c)
MATCH (wo)-[:REPLACED]->(part)
WITH doc, part, collect(DISTINCT wo) AS orders
RETURN doc.title AS guidance, part.partNumber AS partNumber, part.name AS name,
       size(orders) AS timesUsed,
       size([o IN orders WHERE o.comeback]) AS comebacks
ORDER BY comebacks, timesUsed DESC
"""

print(json.dumps(query(CYPHER, vin=vin, code=code), indent=2, default=str))
