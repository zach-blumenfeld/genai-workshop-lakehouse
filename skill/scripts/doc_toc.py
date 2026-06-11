"""Table of contents for a document - what does it cover, in order?

Usage: python skill/scripts/doc_toc.py MAN-FAL-3

The agent uses this to navigate before reading: fetch the shape of a
document, then drill into the relevant section's text.
"""

import json
import sys

from db import query

doc_id = sys.argv[1]

# ============================================================ FILL IN ======
# Walk the document's tree and return each section's id and title with its
# depth, ordered as it appears in the document. Hints:
#   - match the path:  path = (d:Document {id: $doc_id})-[:HAS_SECTION*]->(s)
#   - depth is length(path) - 1
#   - order by [n IN nodes(path) | n.seq]
CYPHER = """
MATCH (d:Document {id: $doc_id})   // <-- complete this pattern
RETURN d.title AS section, 0 AS depth
"""
# ===========================================================================

print(json.dumps(query(CYPHER, doc_id=doc_id), indent=2, default=str))
