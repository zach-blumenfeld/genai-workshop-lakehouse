# AI on Your Lakehouse — workshop environment

Companion environment for the GraphAcademy workshop
**AI on Your Lakehouse: Context Comes in Shapes, Not Queries**.

You build an autonomous **service-advisor agent** for AutoFix Group: a skill
(playbook + scripts) that lets your coding agent decide and act on incoming
work orders, grounded in a graph that spans the lakehouse's documents and
warehouse tables.

## Layout

| Path | What |
|---|---|
| `corpus/` | The document half as authored markdown (`<area>/<id>.md`), the source of truth |
| `sources/pdfs/` | The corpus rendered to PDFs (manuals, bulletins, recall notices) — what the loader parses |
| `sources/warehouse/` | The warehouse half: CSV exports of the BigQuery tables `autofix.service.*` |
| `load/` | The docs-only pipeline: parse the PDF library → one Neo4j **document** graph. `python load/load_documents.py` (warehouse rows stay in BigQuery) |
| `skill/` | **What you build.** The service-advisor skill: `SKILL.md` playbook + `scripts/` tools. Modules 3–4 are fill-in-the-blank; Module 5 is written from the spec in SKILL.md |
| `api/` | Mock parts-ordering API (`uvicorn api.parts_api:app --port 8800`) |
| `events/` | Incoming work-order events for the finale |
| `solutions/` | Complete scripts — catch up or compare |
| `tools/` | Authoring tools: `render_corpus.py` (markdown → PDFs), `generate_warehouse.py` + `generate_events.py` (warehouse CSVs + events from `catalog.frozen.json`) |

## Quick start (the workshop lesson walks through this)

1. Open in a GitHub Codespace (or locally: `pip install -r requirements.txt`,
   install [neo4j-cli](https://github.com/neo4j-labs/neo4j-cli), run
   `neo4j-cli skill install`)
2. Paste your Neo4j sandbox credentials into `.env`
3. `python load/load_documents.py`
4. `uvicorn api.parts_api:app --port 8800` in a second terminal
5. Start your coding agent in the repo root — the skill in `skill/` is the
   agent's playbook

## Swapping in a real lakehouse

The pipeline is source-agnostic by design:

- **Warehouse:** the rows live in BigQuery and are never migrated; the finale
  federates against them with live SQL. Point a different connector at your own
  warehouse and the same shapes work (the connections graph is built by neocarta
  from the information schema — see `connections/build_connections.py`)
- **Documents:** point `load/parse_corpus.py:iter_pdf_paths()` at your storage
  (`PDF_SOURCE=gcs` reads the same folder layout from a bucket)
- Everything downstream — graph model, skill, tools, policy — is unchanged
