r"""Run a BigQuery SQL statement using the workshop's auth.

The agent writes Text2SQL grounded by the `connections` MCP schema, then runs it
here. Auth comes from bq.py: the read-only key in BIGQUERY_SA_KEY_B64 if set,
otherwise your own gcloud login. Use this rather than the `bq` CLI, which does
not read the workshop key.

Usage:
  python skill/scripts/run_sql.py "SELECT model, COUNT(*) AS n
                                    FROM \`PROJECT.DATASET.vehicles\` GROUP BY model"
"""

import json
import sys

from bq import bq_query

if len(sys.argv) < 2:
    sys.exit('usage: run_sql.py "<SQL>"')

rows = bq_query(sys.argv[1])
print(json.dumps(rows, indent=2, default=str))
print(f"\n{len(rows)} rows", file=sys.stderr)
