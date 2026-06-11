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
| `sources/pdfs/` | The document half: manuals, bulletins, recall notices (real PDFs) |
| `sources/warehouse/` | The warehouse half: CSV exports mirroring Delta tables `autofix.service.*` |
| `load/` | The pipeline: parse PDFs + read warehouse → one Neo4j graph. `python load/load_graph.py` |
| `skill/` | **What you build.** The service-advisor skill: `SKILL.md` playbook + `scripts/` tools. Modules 2–3 are fill-in-the-blank; Module 4 is written from the spec in SKILL.md |
| `api/` | Mock parts-ordering API (`uvicorn api.parts_api:app --port 8800`) |
| `events/` | Incoming work-order events for the finale |
| `solutions/` | Complete scripts — catch up or compare |
| `tools/` | Dataset generator (`generate_sources.py` regenerates PDFs + CSVs from `data_def.py`) |

## Quick start (the workshop lesson walks through this)

1. Open in a GitHub Codespace (or locally: `pip install -r requirements.txt`,
   install [neo4j-cli](https://github.com/neo4j-labs/neo4j-cli), run
   `neo4j-cli skill install`)
2. Paste your Neo4j sandbox credentials into `.env`
3. `python load/load_graph.py`
4. `uvicorn api.parts_api:app --port 8800` in a second terminal
5. Start your coding agent in the repo root — the skill in `skill/` is the
   agent's playbook

## Swapping in a real lakehouse

The pipeline is source-agnostic by design:

- **Warehouse:** set `WAREHOUSE_SOURCE=databricks` plus the `DATABRICKS_*`
  variables in `.env` — `load/warehouse_source.py` reads the live Unity
  Catalog tables with the same row contract as the CSVs
- **Documents:** point `load/parse_pdfs.py:iter_pdf_paths()` at your storage
- Everything downstream — graph model, skill, tools, policy — is unchanged
