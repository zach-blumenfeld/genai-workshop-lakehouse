"""Theme cards - the compact context view an agent reasons over.

Usage: python skill/scripts/theme_cards.py

One card per detected theme: its sections, the documents involved, and the
part numbers and trouble codes that hold it together. Six cards summarize
the entire document estate.
"""

import json

from db import query

# ============================================================ FILL IN ======
# For each communityId with more than one member Section, return:
#   theme       - the communityId
#   sections    - count of member sections
#   documents   - DISTINCT titles of documents the members belong to
#   sharedKeys  - DISTINCT part numbers / codes the members reference
# Hints: group with  WITH s.communityId AS theme, collect(s) AS members
#        reach documents with  (d:Document)-[:HAS_SECTION*]->(s)
#        reach keys with  (s)-[:REFERENCES_PART|REFERENCES_CODE]->(k)
#        and  coalesce(k.partNumber, k.code)
CYPHER = """
MATCH (s:Section)
RETURN s.communityId AS theme, count(s) AS sections   // <-- complete
ORDER BY sections DESC
"""
# ===========================================================================

print(json.dumps(query(CYPHER), indent=2, default=str))
