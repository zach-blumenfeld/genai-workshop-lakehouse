"""Parse the AutoFix PDFs and build a Databricks AI Search (Vector Search) index.

The document half of the failure-mode demo, the modern Databricks way:
  1. ai_parse_document() over the PDFs in the UC Volume   -> doc_parsed
  2. explode the parsed output into search-ready chunks    -> doc_chunks (CDF on)
  3. create an AI/Vector Search endpoint (if needed)
  4. create a Delta Sync index over doc_chunks, embedding chunk_text with a
     Foundation-Model embedding endpoint (default databricks-gte-large-en)

Prereqs: run upload_pdfs.py first (PDFs in the Volume). Needs AI Search enabled
and a serverless/SQL warehouse that can run ai_parse_document (GA).

Env (a .env is loaded if present):
  DATABRICKS_SERVER_HOSTNAME / DATABRICKS_HTTP_PATH / DATABRICKS_TOKEN
  DATABRICKS_CATALOG           default: autofix
  DATABRICKS_SCHEMA            default: autofix_service
  DATABRICKS_VOLUME            default: pdfs
  DATABRICKS_VS_ENDPOINT       default: autofix-search
  DATABRICKS_EMBED_ENDPOINT    default: databricks-gte-large-en

Run:  python databricks/build_doc_index.py
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
VOLUME = os.environ.get("DATABRICKS_VOLUME", "pdfs")
VS_ENDPOINT = os.environ.get("DATABRICKS_VS_ENDPOINT", "autofix-search")
EMBED_ENDPOINT = os.environ.get("DATABRICKS_EMBED_ENDPOINT", "databricks-gte-large-en")

FQ = f"`{CATALOG}`.`{SCHEMA}`"
VOL_PATH = f"/Volumes/{CATALOG}/{SCHEMA}/{VOLUME}"
PARSED = f"{FQ}.doc_parsed"
CHUNKS = f"{FQ}.doc_chunks"
INDEX = f"{CATALOG}.{SCHEMA}.doc_chunks_idx"          # VS client wants plain dotted name
SOURCE = f"{CATALOG}.{SCHEMA}.doc_chunks"

# Candidate chunk-extraction strategies (ai_parse_document's nested shape varies
# by version). We try each and keep the first that yields rows.
CHUNK_SQLS = {
    "elements": f"""
        CREATE OR REPLACE TABLE {CHUNKS} TBLPROPERTIES (delta.enableChangeDataFeed = true) AS
        SELECT md5(p.path || '#' || e.pos) AS chunk_id,
               regexp_extract(p.path, '([^/]+)/([^/]+\\\\.pdf)$', 0) AS source,
               e.value:content::string AS chunk_text
        FROM (SELECT path, parse_json(to_json(ai_parse_document(content))) AS pj
              FROM READ_FILES('{VOL_PATH}/**', format => 'binaryFile')) p,
             LATERAL variant_explode(p.pj:document:elements) AS e
        WHERE e.value:content::string IS NOT NULL AND length(e.value:content::string) > 0
    """,
    "pages": f"""
        CREATE OR REPLACE TABLE {CHUNKS} TBLPROPERTIES (delta.enableChangeDataFeed = true) AS
        SELECT md5(p.path || '#' || pg.pos) AS chunk_id,
               regexp_extract(p.path, '([^/]+)/([^/]+\\\\.pdf)$', 0) AS source,
               coalesce(pg.value:representation:markdown::string, pg.value:content::string) AS chunk_text
        FROM (SELECT path, parse_json(to_json(ai_parse_document(content))) AS pj
              FROM READ_FILES('{VOL_PATH}/**', format => 'binaryFile')) p,
             LATERAL variant_explode(p.pj:document:pages) AS pg
        WHERE coalesce(pg.value:representation:markdown::string, pg.value:content::string) IS NOT NULL
    """,
    "wholedoc": f"""
        CREATE OR REPLACE TABLE {CHUNKS} TBLPROPERTIES (delta.enableChangeDataFeed = true) AS
        SELECT md5(path) AS chunk_id,
               regexp_extract(path, '([^/]+)/([^/]+\\\\.pdf)$', 0) AS source,
               to_json(ai_parse_document(content)) AS chunk_text
        FROM READ_FILES('{VOL_PATH}/**', format => 'binaryFile')
    """,
}


def main():
    with sql.connect(server_hostname=HOST, http_path=HTTP_PATH, access_token=TOKEN) as conn:
        cur = conn.cursor()

        # 1) parse -> show one sample so the output schema is visible
        print(f"Parsing PDFs in {VOL_PATH} with ai_parse_document (one-time, ~minutes)...")
        cur.execute(f"""CREATE OR REPLACE TABLE {PARSED} AS
                        SELECT path, ai_parse_document(content) AS parsed
                        FROM READ_FILES('{VOL_PATH}/**', format => 'binaryFile')""")
        cur.execute(f"SELECT count(*) FROM {PARSED}")
        print(f"  parsed {cur.fetchone()[0]} documents into {PARSED}")
        cur.execute(f"SELECT substr(to_json(parsed), 1, 600) FROM {PARSED} LIMIT 1")
        print("  sample parsed (head):", cur.fetchone()[0])

        # 2) chunk -> first strategy that yields rows wins
        chosen = None
        for name, ddl in CHUNK_SQLS.items():
            try:
                cur.execute(ddl)
                cur.execute(f"SELECT count(*) FROM {CHUNKS}")
                n = cur.fetchone()[0]
                print(f"  chunk strategy '{name}': {n} chunks")
                if n > 0:
                    chosen = name
                    break
            except Exception as ex:
                print(f"  chunk strategy '{name}' failed: {str(ex)[:120]}")
        if not chosen:
            raise SystemExit("No chunk strategy produced rows - inspect doc_parsed schema and adjust CHUNK_SQLS.")
        # extend deleted-file retention so scheduled/triggered re-syncs don't fail
        # if more than the default 7 days passes between syncs (VACUUM safety).
        cur.execute(f"ALTER TABLE {CHUNKS} SET TBLPROPERTIES ('delta.deletedFileRetentionDuration' = 'interval 30 days')")
        print(f"  using chunk strategy: {chosen}; table {CHUNKS} ready (CDF on, 30-day retention)")
        cur.close()

    # 3) AI/Vector Search endpoint (idempotent) + 4) Delta Sync index
    from databricks.vector_search.client import VectorSearchClient
    vsc = VectorSearchClient(workspace_url=f"https://{HOST}", personal_access_token=TOKEN, disable_notice=True)

    existing = {e.get("name") for e in vsc.list_endpoints().get("endpoints", [])}
    if VS_ENDPOINT not in existing:
        print(f"Creating Vector/AI Search endpoint '{VS_ENDPOINT}' (provisions, ~minutes)...")
        vsc.create_endpoint_and_wait(name=VS_ENDPOINT, endpoint_type="STANDARD")
    print(f"Endpoint ready: {VS_ENDPOINT}")

    try:
        idx = vsc.get_index(endpoint_name=VS_ENDPOINT, index_name=INDEX)
        print(f"Index {INDEX} already exists; syncing.")
        idx.sync()
    except Exception:
        print(f"Creating Delta Sync index {INDEX} (embeds chunk_text via {EMBED_ENDPOINT}; syncs, ~minutes)...")
        vsc.create_delta_sync_index_and_wait(
            endpoint_name=VS_ENDPOINT,
            index_name=INDEX,
            source_table_name=SOURCE,
            pipeline_type="TRIGGERED",
            primary_key="chunk_id",
            embedding_source_column="chunk_text",
            embedding_model_endpoint_name=EMBED_ENDPOINT,
        )
    print(f"Done: AI Search index {INDEX} is live on endpoint {VS_ENDPOINT}.")


if __name__ == "__main__":
    main()
