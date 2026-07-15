# AI on Your Lakehouse — workshop environment

Companion environment for the GraphAcademy workshop
**AI on Your Lakehouse: Context Comes in Shapes, Not Queries**.

You build a **service-advisor skill** for AutoFix Group: a playbook + scripts that
let your coding agent answer questions about the technical library and the repair
history — grounded in a graph that spans the lakehouse's documents and warehouse
tables.

The data comes in two halves that share keys (part numbers, trouble codes):

- **Documents** — repair manuals, service bulletins, and recall notices (PDFs),
  parsed into a Neo4j **document graph** (a navigable tree plus Leiden themes).
- **Warehouse** — vehicles, work orders, and parts in **BigQuery**. The rows stay
  in BigQuery; **neocarta** reads only their metadata (the foreign-key join paths)
  into a Neo4j **connections** graph, and the agent federates across the two.

## Quick start

### In a Codespace (recommended)

Open the repo in a GitHub Codespace — `.devcontainer/post-create.sh` installs
everything for you: Python dependencies, the Neo4j CLI with its agent skills, and
Claude Code.

→ [Open in GitHub Codespace](https://github.com/codespaces/new/zach-blumenfeld/genai-workshop-lakehouse)

### Locally

```bash
git clone https://github.com/zach-blumenfeld/genai-workshop-lakehouse
cd genai-workshop-lakehouse
./.devcontainer/post-create-local.sh   # isolated venv + deps + neo4j-cli + agent skills
source .venv/bin/activate
```

Then add your credentials to `.env` (the setup script copies it from
`.env.example`):

- **Neo4j** — a sandbox with the Graph Data Science library (a
  [GDS blank sandbox](https://sandbox.neo4j.com) works). Paste `NEO4J_URI`,
  `NEO4J_USERNAME`, `NEO4J_PASSWORD`, `NEO4J_DATABASE`.
- **BigQuery** — the workshop dataset is read-only; use the one-line
  `BIGQUERY_SA_KEY_B64` from the workshop, or use your own `gcloud` login. To
  provision your own copy of the warehouse, see [`bigquery/`](bigquery/).
- **Anthropic** — set `ANTHROPIC_API_KEY`, or leave it blank to use your Claude
  Code subscription.

## The workshop flow

The GraphAcademy course walks through each step; here are the commands per module.

1. **Connections (Module 2)** — build the warehouse's join-path graph:
   ```bash
   python load/build_connections.py
   ```
   Approve the `connections` MCP in your agent, then ask a warehouse question and
   watch it retrieve the schema and write Text2SQL (run with
   `python skill/scripts/run_sql.py "<SQL>"`).
2. **Trees (Module 3)** — load the documents, then build the navigation tools:
   ```bash
   python load/load_documents.py
   ```
   Fill the `BUILD FROM SPEC` blocks in `skill/scripts/outline.py` and `search.py`
   (spec: `docs/outline-format.md`).
3. **Themes (Module 4)** — fill `skill/scripts/themes.py` (spec:
   `docs/theme-format.md`) and run it; `--gamma` dials theme granularity.
4. **Finale (Module 6)** — answer the questions that run the shop by combining the
   shapes. Start your agent and ask, for example:
   - *"For VIN FAL20T20220002 with code P0301: what fixed this on similar vehicles?"*
   - *"What are the common patterns across all our bulletins and recalls?"*
   - *"Which fault codes are failing in the field but have no documentation?"*

Start your coding agent in the repo root — `skill/SKILL.md` is its playbook.

## Layout

| Path | What |
|---|---|
| `corpus/` | The document half as authored markdown (`<area>/<id>.md`), the source of truth |
| `sources/pdfs/` | The corpus rendered to PDFs (manuals, bulletins, recalls) — what the loader parses |
| `sources/warehouse/` | CSV exports of the BigQuery tables `autofix.service.*` |
| `load/` | The pipelines: `build_connections.py` (warehouse metadata graph) and `load_documents.py` (document graph) |
| `skill/` | **What you build** — the service-advisor skill: `SKILL.md` playbook + `scripts/` tools |
| `solutions/` | Complete scripts — catch up or compare |
| `docs/` | The shape specs (`outline-format.md`, `theme-format.md`) you build against |
| `bigquery/` | Provision your own copy of the AutoFix warehouse in BigQuery |
| `databricks/` | Optional: stand the same data up on Databricks (Genie + AI Search) |
| `tools/` | Authoring tools: `render_corpus.py` (markdown → PDFs), `generate_warehouse.py` (warehouse CSVs) |

## Running it locally

The loaders are idempotent, but to wipe the graph and start clean:

```bash
neo4j-cli query --uri "$NEO4J_URI" --username "$NEO4J_USERNAME" --password "$NEO4J_PASSWORD" \
  "MATCH (n) DETACH DELETE n" --rw
neo4j-cli query --uri "$NEO4J_URI" --username "$NEO4J_USERNAME" --password "$NEO4J_PASSWORD" \
  "DROP INDEX content_search IF EXISTS" --rw
```

Stuck? `solutions/scripts/` has every completed tool. Themes need GDS (a GDS
sandbox has it); a crashed themes run cleans up its own projection.

## Swapping in a real lakehouse

The pattern is source-agnostic:

- **Warehouse** — point neocarta at your own warehouse (declared keys → the same
  connections graph). The rows stay put; the agent federates with live SQL. Or
  stand the data up on **Databricks** (Genie + AI Search) — see [`databricks/`](databricks/).
- **Documents** — point `load/parse_corpus.py:iter_pdf_paths()` at your storage
  (`PDF_SOURCE=gcs` reads the same folder layout from a bucket).
- Everything downstream — graph model, skill, and tools — is unchanged.
