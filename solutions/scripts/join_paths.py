"""SOLUTION: join neighbors of a warehouse table, from the connections graph.

Usage: python solutions/scripts/join_paths.py <table>

Reads neocarta's metadata graph: which tables this one joins to, and on which
key. Chain these to compose a multi-table join — this is how the agent grounds
the SQL it sends to BigQuery in the finale.
"""

import sys
from db import query

table = sys.argv[1]

CYPHER = """
MATCH (t:Table {name: $table})-[:HAS_COLUMN]->(c)-[:REFERENCES]->(c2)<-[:HAS_COLUMN]-(o:Table)
RETURN t.name AS from_table, c.name AS join_key, o.name AS to_table, 'out' AS direction
UNION
MATCH (t:Table {name: $table})-[:HAS_COLUMN]->(c)<-[:REFERENCES]-(c2)<-[:HAS_COLUMN]-(o:Table)
RETURN o.name AS from_table, c2.name AS join_key, t.name AS to_table, 'in' AS direction
"""

import json
print(json.dumps(query(CYPHER, table=table), indent=2, default=str))
