"""SOLUTION: Theme cards - the compact context view an agent reasons over."""
import json
from db import query

CYPHER = """
MATCH (s:Section)
WITH s.communityId AS theme, collect(s) AS members
WHERE size(members) > 1
UNWIND members AS s
MATCH (d:Document)-[:HAS_SECTION*]->(s)
OPTIONAL MATCH (s)-[:REFERENCES_PART|REFERENCES_CODE]->(k)
WITH theme, count(DISTINCT s) AS sections,
     collect(DISTINCT d.title) AS documents,
     collect(DISTINCT coalesce(k.partNumber, k.code)) AS sharedKeys
RETURN theme, sections, documents, sharedKeys
ORDER BY sections DESC
"""

print(json.dumps(query(CYPHER), indent=2, default=str))
