"""SOLUTION: Open recalls this vehicle is in scope for but never received.

Usage: python solutions/scripts/recall_exposure.py CM-FAL-2020-0451

Scope is matched by model; the recall's own Defect/Remedy text is the
authority on years and variants - read the grounding sections to confirm
before bundling. The remedy part is the current (non-superseded) part the
recall's sections reference.
"""

import json
import sys

from db import query

vin = sys.argv[1]

CYPHER = """
MATCH (v:Vehicle {vin: $vin})
MATCH (r:RecallNotice {model: v.model})-[:HAS*]->(sec:Section)
      -[:REFERENCES_PART]->(remedy:Part)
WHERE NOT (remedy)-[:SUPERSEDED_BY]->()
  AND NOT EXISTS {
    (v)-[:HAS_WORK_ORDER]->(:WorkOrder)-[:REPLACED]->(remedy)
  }
RETURN DISTINCT r.id AS recall, r.title AS title,
       remedy.partNumber AS remedyPart,
       collect(DISTINCT sec.uri) AS groundingSections
"""

print(json.dumps(query(CYPHER, vin=vin), indent=2, default=str))
