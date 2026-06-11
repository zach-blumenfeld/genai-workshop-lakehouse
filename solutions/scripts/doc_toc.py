"""SOLUTION: Table of contents for a document."""
import json
import sys
from db import query

doc_id = sys.argv[1]

CYPHER = """
MATCH path = (d:Document {id: $doc_id})-[:HAS_SECTION*]->(s:Section)
RETURN s.id AS id, s.title AS section, length(path) - 1 AS depth
ORDER BY [n IN nodes(path) | n.seq]
"""

print(json.dumps(query(CYPHER, doc_id=doc_id), indent=2, default=str))
