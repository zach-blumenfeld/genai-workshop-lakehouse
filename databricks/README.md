# Set up AutoFix on Databricks (Genie + AI Search)

The workshop's default backend is BigQuery (warehouse) + Neo4j (graph). This
folder is an **optional alternative**: it stands the same AutoFix data up on
**Databricks** and exposes it to a coding agent through Databricks' managed MCP -
**Genie** over the warehouse tables and **AI Search** over the document PDFs.

Use it if you would rather run the AutoFix data on Databricks, or to see how the
pattern ports to another lakehouse.

---

## Prereqs

- **Project venv** with: `databricks-sql-connector`, `databricks-sdk`,
  `databricks-ai-search` (aka `databricks-vectorsearch`), `python-dotenv`
  (all installed by the workshop setup).
- **`.env`** (the scripts read these internally - never commit it):
  ```
  DATABRICKS_SERVER_HOSTNAME=dbc-xxxx.cloud.databricks.com   # no https://
  DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/<id>             # a SQL warehouse
  DATABRICKS_TOKEN=dapi...
  DATABRICKS_CATALOG=lakehouse-workshop
  DATABRICKS_SCHEMA=autofix_service
  # optional: DATABRICKS_VOLUME=pdfs  DATABRICKS_VS_ENDPOINT=autofix-search  DATABRICKS_EMBED_ENDPOINT=databricks-gte-large-en
  ```
- **Workspace features:** Unity Catalog; a running **SQL warehouse**; **AI Search**
  enabled with an embedding endpoint (`databricks-gte-large-en`); **managed MCP**
  (Public Preview); and a **Genie space** for the table tool. A served chat model
  for Genie/agents (e.g. `databricks-claude-sonnet-4-5`).

> If `DATABRICKS_CATALOG` isn't in `.env`, the scripts default to `autofix`; prepend
> it inline, e.g. `DATABRICKS_CATALOG=lakehouse-workshop python databricks/load_databricks.py`.

---

## Part A - Build the data

Run from the repo root. (`test_connection.ipynb` is a quick `.env` connection
smoke test if you want to confirm credentials first.)

| Step | Command | Result |
|---|---|---|
| 1 | `python databricks/load_databricks.py` | 6 Delta tables in `{catalog}.{schema}` with PK/FK constraints (idempotent). |
| 2 | `python databricks/upload_pdfs.py` | UC Volume `{catalog}.{schema}.pdfs` + the AutoFix PDFs uploaded. |
| 3 | `python databricks/build_doc_index.py` | `ai_parse_document` → `doc_chunks` (CDF) → **AI Search endpoint + Delta Sync index** (embeds via `databricks-gte-large-en`). **Provisions infra, ~10-20 min, billed.** |

---

## Part B - Expose the tools as managed MCP

The agent reaches these over Databricks managed MCP (`/api/2.0/mcp/...`, Public Preview).

1. **AI Search MCP** - ready once the index is live. URL:
   ```
   https://<host>/api/2.0/mcp/ai-search/lakehouse-workshop/autofix_service/doc_chunks_idx
   ```
2. **Genie Space MCP** *(create in the UI)* - a **Genie space** scoped to the
   **6 warehouse tables**: `vehicles`, `work_orders`, `work_order_parts`,
   `parts`, `procedures`, `dtc_codes`. Copy its `space_id`:
   ```
   https://<host>/api/2.0/mcp/genie/<space_id>
   ```
3. Confirm **managed MCP** is enabled for the workspace (admin; Public Preview).

---

## Part C - Wire the tools into your coding agent

User-scoped so the token never lands in the repo. Replace `<host>`, `<space_id>`, `<PAT>`:

```
claude mcp add --transport http databricks-aisearch \
  https://<host>/api/2.0/mcp/ai-search/lakehouse-workshop/autofix_service/doc_chunks_idx \
  --header "Authorization: Bearer <PAT>"

claude mcp add --transport http databricks-genie \
  https://<host>/api/2.0/mcp/genie/<space_id> \
  --header "Authorization: Bearer <PAT>"
```

Then start your agent and **approve** both servers when prompted. (OAuth is the
preferred managed-MCP auth; a PAT bearer is simplest to get going. Don't commit the token.)

---

## Teardown (stop billing)

The AI Search endpoint bills while running:
```python
from databricks.vector_search.client import VectorSearchClient
vsc = VectorSearchClient(workspace_url="https://<host>", personal_access_token="<token>", disable_notice=True)
vsc.delete_index(endpoint_name="autofix-search", index_name="lakehouse-workshop.autofix_service.doc_chunks_idx")
vsc.delete_endpoint("autofix-search")
```
Full reset: `DROP SCHEMA \`lakehouse-workshop\`.\`autofix_service\` CASCADE` (drops the
tables, Volume, parsed/chunk tables). Remove the MCP servers with
`claude mcp remove databricks-aisearch databricks-genie`.

---

## Files

| File | Role |
|---|---|
| `test_connection.ipynb` | `.env` / connection smoke test |
| `load_databricks.py` | warehouse → 6 Delta tables |
| `upload_pdfs.py` | PDFs → UC Volume |
| `build_doc_index.py` | parse → chunks → AI Search endpoint + index |
| `README.md` | this guide |
