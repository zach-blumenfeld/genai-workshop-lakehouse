# Databricks failure-mode demo — walkthrough

Stand up the AutoFix data on Databricks and run the **failure mode**: a frontier
coding agent, given Databricks' *best* managed tools, can't reliably answer the
canonical cross-boundary question — while the **same agent** over the graph does
it in one deterministic, auditable traversal.

> **The experiment — hold the agent constant, swap the substrate.**
> The course uses **Claude Code** throughout. So we use Claude Code for *both* arms
> and change only the data shape:
> - **Databricks arm:** Claude Code → Databricks **managed MCP** (Genie space + AI Search index).
> - **Graph arm:** Claude Code → the Neo4j graph + BigQuery federation (the course skill).
>
> Same agent, same MCP mechanism, different shape. That isolates the variable to *the
> shape* (the thesis) and is robust to "you used a weak agent" (it's frontier) and
> "you didn't build it the Databricks way" (it's Genie + AI Search via Databricks'
> own managed MCP). We deliberately do **not** use Databricks Agent Bricks as the
> orchestrator — that would conflate agent quality with substrate.

**Why it fails / positioning / deep detail:** see **`databricks-failure-mode-demo.md`**
(the canonical query needs the doc↔table boundary crossed on a shared key — a part
number that is *text in a PDF*, not a column — and Genie + AI Search are two
*probabilistic* retrievers that don't cross it reliably).

---

## Prereqs

- **Project venv** with: `databricks-sql-connector`, `databricks-sdk`,
  `databricks-ai-search` (aka `databricks-vectorsearch`), `python-dotenv` (and
  `openai` only if you use the optional bespoke loop). All already installed here.
- **`.env`** (the scripts read these internally — never commit it):
  ```
  DATABRICKS_SERVER_HOSTNAME=dbc-xxxx.cloud.databricks.com   # no https://
  DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/<id>             # a SQL warehouse
  DATABRICKS_TOKEN=dapi...
  DATABRICKS_CATALOG=lakehouse-workshop
  DATABRICKS_SCHEMA=autofix_service
  # optional: DATABRICKS_VOLUME=pdfs  DATABRICKS_VS_ENDPOINT=autofix-search  DATABRICKS_EMBED_ENDPOINT=databricks-gte-large-en
  ```
- **Workspace features:** Unity Catalog; a running **SQL warehouse**; **AI Search**
  enabled; an embedding endpoint (`databricks-gte-large-en`); **managed MCP**
  (Public Preview); and — for the table tool — a **Genie space**. A served chat
  model exists for Genie/agents (e.g. `databricks-claude-sonnet-4-5`).

> If `DATABRICKS_CATALOG` isn't in `.env`, the scripts default to `autofix`; prepend
> it inline, e.g. `DATABRICKS_CATALOG=lakehouse-workshop python databricks/load_databricks.py`.

---

## Part A — Build the data (terminal scripts)

Run from the repo root. (`test_connection.ipynb` is a quick `.env` smoke test if unsure.)

| Step | Command | Result |
|---|---|---|
| 1 | `python databricks/load_databricks.py` | 6 Delta tables in `{catalog}.{schema}` with PK/FK constraints (idempotent). |
| 2 | `python databricks/upload_pdfs.py` | UC Volume `{catalog}.{schema}.pdfs` + 183 PDFs uploaded. |
| 3 | `python databricks/build_doc_index.py` | `ai_parse_document` → `doc_chunks` (CDF, 30-day retention) → **AI Search endpoint + Delta Sync index** (embeds via `databricks-gte-large-en`). **Provisions infra, ~10–20 min, billed.** |

**Sanity-check the raw tools** (not the demo — just proves SQL + AI Search return):
```
python databricks/run_failure_demo.py
```
It prints the deterministic 4-table SQL answer (the **grading oracle**:
`IC-2042-B`, 0 comebacks) next to raw AI Search hits.

---

## Part B — Expose Databricks' tools as managed MCP

The agent reaches these over Databricks managed MCP (`/api/2.0/mcp/...`, Public Preview).

1. **AI Search MCP** — ready now (the index is live). URL:
   ```
   https://<host>/api/2.0/mcp/ai-search/lakehouse-workshop/autofix_service/doc_chunks_idx
   ```
2. **Genie Space MCP** *(you, in the UI)* — create a **Genie space** scoped to the
   **6 warehouse tables only**: `vehicles`, `work_orders`, `work_order_parts`,
   `parts`, `procedures`, `dtc_codes`. **Do _not_ add `doc_chunks` / `doc_parsed`** —
   documents belong to the AI Search MCP; keeping them out preserves the doc↔table
   boundary the demo is about. (Steelman it: add a **Metric View** for the work-order
   metrics and connect the **Genie Ontology**.) Copy its `space_id`:
   ```
   https://<host>/api/2.0/mcp/genie/<space_id>
   ```
3. Confirm **managed MCP** is enabled for the workspace (admin; Public Preview).

---

## Part C — Wire the tools into Claude Code (the course agent)

User-scoped so the token never lands in the repo (per the course's `.mcp.json`
pattern for the Neo4j `connections` MCP). Replace `<host>`, `<space_id>`, `<PAT>`:

```
claude mcp add --transport http databricks-aisearch \
  https://<host>/api/2.0/mcp/ai-search/lakehouse-workshop/autofix_service/doc_chunks_idx \
  --header "Authorization: Bearer <PAT>"

claude mcp add --transport http databricks-genie \
  https://<host>/api/2.0/mcp/genie/<space_id> \
  --header "Authorization: Bearer <PAT>"
```
Then start Claude Code and **approve** both servers when prompted. (OAuth is the
preferred managed-MCP auth; a PAT bearer is simplest for a demo. Don't commit the token.)

---

## Part D — Run the failure mode

Give Claude Code this prompt (use **only** the Databricks MCP tools), in a **fresh
session**, **3–5 times**:

> *A 2021 Falcon with the 2.0T engine is in the shop with diagnostic trouble code
> P0301 (cylinder-1 misfire), VIN `FAL20T20220002`. Using only the AI Search service
> documents and the Genie warehouse, recommend the specific replacement part with the
> best real-world repair outcomes for this code on cars like this, justify it with the
> repair history (comebacks), and tell me whether this vehicle has any open safety
> recall it has not received. Cite your evidence.*

**Capture per run:** the SQL Genie generates; whether the 4-table join + comeback
ranking is correct; whether it ever ties the bulletin's part (`IC-2042-A → IC-2042-B`)
to the warehouse `part_number`; and whether the recommendation is **consistent across runs**.

**Grading oracle (correct answer):** part **`IC-2042-B`** (18 uses, **0 comebacks**);
open recall **`rc-2021-11`** (alternator stall, `ALT-8810`) this VIN hasn't received.
The deterministic SQL that produces it is in `run_failure_demo.py`.

**Expected failures** (detail in `databricks-failure-mode-demo.md` §4): AI Search ranks
a near-miss bulletin above the right one and never ties applicability to *this* VIN;
Genie's multi-table join is non-deterministic / sometimes wrong; the part↔row boundary
is crossed (if at all) only by the LLM guessing in prose — no single auditable path.

---

## Part E — The contrast (the course finale)

Same prompt to Claude Code with the **Neo4j graph + federation skill** (the course's
`autofix-service-advisor`): one deterministic traversal grounds the code in the
documents, reads the live repair outcomes from BigQuery on the shared key, and returns
`IC-2042-B` + the recall — **the same, inspectable answer every run.**

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
| `run_failure_demo.py` | raw-tool sanity check + grading oracle (not the demo) |
| `databricks-failure-mode-demo.md` | positioning brief + the modern-stack detail + what to capture |
| `README.md` | this walkthrough |
