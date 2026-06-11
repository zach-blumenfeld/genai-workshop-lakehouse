"""Find every document that covers a diagnostic trouble code.

Usage: python skill/scripts/applicable_docs.py P0301

Returns one row per document with the sections that mention the code -
the grounding for any recommendation the agent makes.
"""

import json
import sys

from db import query

code = sys.argv[1]

# ============================================================ FILL IN ======
# Match every Document whose tree contains a Section that references the
# DTC node for $code. Return the document id, docType, and title, plus a
# collected list of the matching section titles.
#
# You need: the variable-length tree pattern  -[:HAS_SECTION*]->
#           the reference pattern             -[:REFERENCES_CODE]->
CYPHER = """
MATCH (d:Document)            // <-- complete this pattern
RETURN d.id AS doc, d.docType AS type, d.title AS title
"""
# ===========================================================================

print(json.dumps(query(CYPHER, code=code), indent=2, default=str))
