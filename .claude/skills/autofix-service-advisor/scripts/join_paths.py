"""join_paths - which tables does a warehouse table join to, and on what key?

Usage: python skill/scripts/join_paths.py <table>

Reads neocarta's connections graph (the metadata Database/Schema/Table/Column
graph with Column-[:REFERENCES]->Column foreign keys). Chaining these neighbors
composes a multi-table join — the grounding for the SQL the agent sends to
BigQuery in the finale. Spec: docs/connections-format.md.
"""

import json
import sys
from db import query

table = sys.argv[1]

# ============================================================ BUILD FROM SPEC =
# Return one row per table that joins to $table, with the join key. The metadata
# graph models a foreign key as:
#   (Table)-[:HAS_COLUMN]->(Column)-[:REFERENCES]->(Column)<-[:HAS_COLUMN]-(Table)
# Cover BOTH directions: keys on $table that reference others (out), and other
# tables whose keys reference $table (in). Return: from_table, join_key,
# to_table, direction ('out'|'in'). Hint: a UNION of the two patterns.
CYPHER = """
MATCH (t:Table {name: $table})
RETURN t.name AS from_table, '' AS join_key, '' AS to_table, '' AS direction
"""
# =============================================================================

print(json.dumps(query(CYPHER, table=table), indent=2, default=str))
