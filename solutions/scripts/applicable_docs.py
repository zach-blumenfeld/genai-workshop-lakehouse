"""SOLUTION: Find every document that covers a diagnostic trouble code."""
import json
import sys
from db import query

code = sys.argv[1]

CYPHER = """
MATCH (d:Document)-[:HAS_SECTION*]->(s:Section)-[:REFERENCES_CODE]->(:DTC {code: $code})
RETURN d.id AS doc, d.docType AS type, d.title AS title,
       collect(s.title) AS sections
"""

print(json.dumps(query(CYPHER, code=code), indent=2, default=str))
