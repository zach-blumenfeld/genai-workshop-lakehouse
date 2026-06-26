"""Run the Databricks failure-mode demo: similarity retrieval vs. deterministic truth.

Shows the two halves a modern Databricks agent fuses, and where the seam fails:
  - GROUND TRUTH (deterministic): the 4-table SQL join answers "what fixed
    <code> on cars like this <model>+<engine>?" exactly, the same every run.
  - AI SEARCH (similarity): vector retrieval over the PDF chunks returns the
    top-k *most similar* chunks for the question - not "the bulletin that applies
    to THIS vehicle + the part that supersedes the old one". Re-run it and the
    boundary (PDF applicability text -> warehouse rows) is never crossed reliably.

This script demonstrates the raw retrievers + the determinism contrast. The full
agent (Genie + AI Search fused via Agent Framework / managed MCP) is the UI/
notebook layer - see databricks-failure-mode-demo.md.

Env: same as the other scripts (DATABRICKS_* + DATABRICKS_VS_ENDPOINT,
DATABRICKS_CATALOG, DATABRICKS_SCHEMA).

Run:  python databricks/run_failure_demo.py
"""

import os

from dotenv import load_dotenv
from databricks import sql

load_dotenv(override=True)

HOST = os.environ["DATABRICKS_SERVER_HOSTNAME"]
HTTP_PATH = os.environ["DATABRICKS_HTTP_PATH"]
TOKEN = os.environ["DATABRICKS_TOKEN"]
CATALOG = os.environ.get("DATABRICKS_CATALOG", "autofix")
SCHEMA = os.environ.get("DATABRICKS_SCHEMA", "autofix_service")
VS_ENDPOINT = os.environ.get("DATABRICKS_VS_ENDPOINT", "autofix-search")
INDEX = f"{CATALOG}.{SCHEMA}.doc_chunks_idx"
FQ = f"`{CATALOG}`.`{SCHEMA}`"

MODEL, ENGINE, CODE = "Falcon", "2.0T", "P0301"
QUESTION = f"What fixed {CODE} misfire on a {MODEL} {ENGINE}?"


def ground_truth():
    print(f"\n=== GROUND TRUTH (deterministic 4-table join) — what fixed {CODE} on {MODEL} {ENGINE} ===")
    q = f"""
    SELECT wop.part_number,
           COUNT(DISTINCT wo.wo_id) AS times_used,
           SUM(CASE WHEN wo.comeback THEN 1 ELSE 0 END) AS comebacks
    FROM {FQ}.work_orders wo
    JOIN {FQ}.vehicles v ON wo.vin = v.vin
    JOIN {FQ}.work_order_parts wop ON wop.wo_id = wo.wo_id
    JOIN {FQ}.parts p ON p.part_number = wop.part_number
    WHERE v.model = '{MODEL}' AND v.engine = '{ENGINE}' AND wo.dtc_code = '{CODE}'
    GROUP BY wop.part_number ORDER BY comebacks ASC, times_used DESC
    """
    with sql.connect(server_hostname=HOST, http_path=HTTP_PATH, access_token=TOKEN) as conn:
        with conn.cursor() as cur:
            cur.execute(q)
            rows = cur.fetchall()
    for r in rows:
        print(f"   {r[0]:12} used={r[1]:3} comebacks={r[2]}")
    if rows:
        print(f"   -> evidence-backed fix: {rows[0][0]} (fewest comebacks). Identical every run.")


def ai_search():
    print(f"\n=== AI SEARCH (similarity over PDF chunks) — query: {QUESTION!r} ===")
    from databricks.vector_search.client import VectorSearchClient
    vsc = VectorSearchClient(workspace_url=f"https://{HOST}", personal_access_token=TOKEN, disable_notice=True)
    try:
        idx = vsc.get_index(endpoint_name=VS_ENDPOINT, index_name=INDEX)
    except Exception as e:
        print(f"   index {INDEX} not ready yet ({str(e)[:80]}). Run build_doc_index.py first.")
        return
    for q in [QUESTION, f"{MODEL} {ENGINE} {CODE} misfire repair", "ignition coil supersession"]:
        res = idx.similarity_search(query_text=q, columns=["source", "chunk_text"], num_results=4)
        hits = (res.get("result", {}) or {}).get("data_array", []) or []
        print(f"\n   query: {q!r}")
        for h in hits:
            src = h[0]
            snippet = " ".join(str(h[1]).split())[:90]
            print(f"     [{src}]  {snippet}…")
    print("\n   ^ top-k *similar* chunks. Note what is NOT delivered: which bulletin applies to")
    print("     THIS vehicle, the part supersession, and the real comeback evidence — that needs")
    print("     the boundary crossed to the warehouse on a shared key, which similarity does not do.")


def main():
    print("DATABRICKS FAILURE-MODE DEMO  (catalog:", CATALOG, "schema:", SCHEMA, ")")
    ground_truth()
    ai_search()
    print("\nThe graph finale answers the whole question in one deterministic, auditable traversal;")
    print("the Databricks stack stitches two probabilistic retrievers across the boundary.")


if __name__ == "__main__":
    main()
