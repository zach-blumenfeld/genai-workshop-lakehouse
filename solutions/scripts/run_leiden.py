"""SOLUTION: Detect document themes with Leiden community detection."""
import sys
from db import query

gamma = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5

query("CALL gds.graph.drop('doc-links', false)")

PROJECT = """
CALL gds.graph.project(
  'doc-links',
  'Section',
  {LINKS_TO: {orientation: 'UNDIRECTED', properties: 'strength'}}
)
"""

WRITE = """
CALL gds.leiden.write('doc-links', {
  writeProperty: 'communityId',
  relationshipWeightProperty: 'strength',
  gamma: $gamma
})
YIELD communityCount, nodeCount
RETURN communityCount, nodeCount
"""

query(PROJECT)
result = query(WRITE, gamma=gamma)
print(f"gamma={gamma}: {result[0]['communityCount']} communities over {result[0]['nodeCount']} sections")
