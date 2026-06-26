# Course Plan — AI on Your Lakehouse: Context Comes in Shapes, Not Queries

## Abstract

*Official course description (source of truth: `course.adoc` — keep in sync).*

**Caption:** Give your agent the shapes its answers need — across documents in Neo4j and a warehouse in BigQuery.

Your agent can reach your data but still can't use it reliably. Vector search and Text2SQL each hand it
a slice, but not the view to know what is truly relevant and how to connect the right information.
Without that, answers come back confident but wrong. That is not a model or query problem — it is a
context problem, and thinking in terms of *shapes* is what cracks it.

In this hands-on workshop, you give an agent three reusable shapes — and learn a second axis: *where
each shape should live*.

- **Connections (Paths)** — how the warehouse tables join, read from BigQuery by neocarta
- **Table of Contents (Trees)** — navigate the documents
- **Themes (Communities)** — surface patterns nobody named

You will work with data from AutoFix Group, a fictional national auto-repair chain: service manuals,
bulletins, and recall notices as PDFs in cloud storage, and vehicles, work orders, parts, and
procedures in a BigQuery warehouse. The two halves share part numbers and diagnostic trouble codes —
and that overlap is what you build on.

You build the shapes the way you would on the job: in a hosted Codespace, you and your coding agent
author a *service-advisor skill* — tools and policy, module by module — and finish by handing it a live
work order. The agent grounds the symptom in the documents, reads the real repair history from
BigQuery, picks the evidence-backed fix, catches an open recall, orders the part through an API, and
leaves an auditable trail in the graph.

At the heart of it is the question Text2SQL gets quietly wrong — "what fixed this code on cars like
this one?" — answered by *federating*: the documents are a graph in Neo4j, the warehouse rows stay in
BigQuery, and the agent crosses the boundary on the shared key. Nothing is migrated that does not need
to be. The pattern is BigQuery-first but portable: swap the connector and the same shapes work on
Snowflake, Databricks, or anywhere your data lives.

---

**Scope.** This doc is the durable plan for the **build environment** — pipeline, skill, scripts,
build state, work tracking. The **course design** (thesis, architecture, document/connections/recommendation
models, module structure, story spine, the 3 finale events, learning outcomes, verification) is owned by
**`asciidoc/courses/workshop-lakehouse/WORKSHOP-PLAN.md`** in `neo4j-graphacademy/courses`. Keep the two
consistent; do not duplicate WORKSHOP-PLAN here — cross-reference it. Actionable work lives in **GitHub
issues prefixed `lakehouse-workshop:`** (label `lakehouse-workshop`), not in this file — see
[Work tracking](#work-tracking).

- **Course content (design authority):** `neo4j-graphacademy/courses` → `asciidoc/courses/workshop-lakehouse/`
  (`:status: draft`; content aligned & verified end-to-end). Design plan: `WORKSHOP-PLAN.md`.
- **Build environment:** `zach-blumenfeld/genai-workshop-lakehouse` (this repo — Codespace, pipeline, skill, specs)
- **Status:** shape-first version shipped (`v1.47.12`); **neocarta/BigQuery restructure + domain-agnostic
  rework SHIPPED** — federated finale runnable, full Codespace runthrough green. Remaining items are infra/release
  only (BigQuery read-auth in Codespace, artwork, prod release, `:status: active`).

---

## Drift log — from the original AIEWF brief to now

Baseline: `~/Documents/content-research-wiki/outputs/lakehouse-workshop-usecase-and-outline.md`
(the 90-minute AI Engineer World's Fair run-of-show). Every change below is deliberate.

### Already shipped — the shape-first rework (`v1.47.12`, live)

- **90 min → 2 hr**; AIEWF one-off → **GraphAcademy hosted + self-paced** (GitHub Codespace)
- **Notebooks + Data Importer → a coding agent + neo4j-cli + a Python skill participants build**
  (`autofix-service-advisor`). "Guided walkthrough" → **everything hands-on, build-from-spec**
- Finale is no longer "multi-hop Cypher + take-home" — it's an **agent that decides *and acts***:
  orders parts through a mock API, writes an auditable `Recommendation` trail, **escalates when
  evidence is thin**
- **Shape-first became the explicit method**: read the spec (`docs/outline-format.md`,
  `docs/theme-format.md`) → derive the graph reasoning → build. Added a **search** shape-tool
  (hierarchical fulltext + agent-side semantic expansion) not in the baseline
- **Louvain → Leiden** (conductance-backed cohesion words, `gamma` granularity dial)

### Shipped — neocarta + federation + domain-agnostic rework (done)

This restructure is **complete and verified end-to-end** (full Codespace runthrough green).
The course-design detail lives in `WORKSHOP-PLAN.md` ("Drift fixed — 2026-06"); the build-env-relevant
changes are:

- **Module reorder shipped:** connections/paths moved from **last → first**. Order is now
  connections → trees → themes → federated finale → wrap (+ optional neo4j-cli in M4).
- **neocarta is the connections tool**, over **BigQuery** (Databricks/Snowflake are portability targets only).
  Exposed via the `connections` MCP server (wired in `.mcp.json`).
- **Architecture is federate, not migrate.** The baseline's *"load the Delta warehouse via Data Importer,
  merge on the shared key"* is **removed.** Warehouse rows stay in BigQuery; only neocarta's connections
  metadata graph loads; the finale federates (live BigQuery SQL + Neo4j full-text grounding). See
  [Architecture](#architecture).
- **Document model went domain-agnostic** (superseding the earlier ki-style/shared-key model). Now
  `Library → Folder → Document → Section`, single `HAS` type, `NEXT_SECTION` reading order, and `LINKS_TO`
  = the author's *real* cross-references (with `{external:true}` URL stubs). **No** `:Part`/`:DTC`/
  `:Bulletin`/`:Manual`/`:RecallNotice`, **no** `REFERENCES_PART`/`REFERENCES_CODE`, **no** `HAS_SECTION`
  (it's `HAS`), **no** `docType`/`citation`/`derived`/`sharedKeys`. Part numbers & DTC codes live in
  section **text** + BigQuery, found by full-text. `Document.id` = slug, `Document.area` = folder.
- **Corpus rebuilt and scaled** from a hand-authored ~10-doc set to a **183-doc** generated corpus.
- **Dead v1 pipeline removed:** `load_graph.py`, `parse_pdfs.py`, `tools/warehouse_source.py`,
  `tools/data_def.py`, `tools/generate_sources.py`. `build_connections.py` moved `connections/` → `load/`.
- **Integrated-sandbox path dropped (Option A):** the `data/` CSV dataset that loaded the warehouse *into*
  Neo4j contradicted federation. Removed; **Codespace + BigQuery is the only path.**
- **New second axis to the thesis:** not just *what* shape, but *where it lives* — derive vs. federate.

### Carried forward (still valid)

The three-layer-wall framing; personas Dani Reyes / Morgan Tao / Sam Okafor; the
determinism / auditability presenter note (a graph beats orchestrated vector+SQL not on
capability but on *one deterministic, auditable traversal*).

---

## Goals & thesis

Build a copilot that can actually *use* a lakehouse — not by picking "search the docs" or "query
the tables," but by giving the agent the **shapes** its answers need.

Two axes:

1. **Context comes in shapes, not queries.** Three reusable shapes:
   - **Connections (paths)** — how structured records join (the warehouse's foreign-key graph)
   - **Trees** — how documents are structured (navigable table of contents)
   - **Themes (communities)** — patterns nobody named, across documents
2. **Where each shape should live — derive vs. federate.** Derive a graph where you own the data or
   nothing else structures it (the documents); keep a metadata/connections graph and **federate**
   where a system of record already owns the rows (the warehouse). This is the decision neocarta
   exists to make, and it is now a taught outcome.

Each maps to one layer of Sam's wall:

| Wall | Failure | Shape that fixes it |
|------|---------|---------------------|
| Vector search | right meaning, wrong shape | document **trees** + **themes** |
| Text2SQL | quietly wrong on multi-hop joins | neocarta **connections** graph grounds the routing |
| Neither crosses the boundary | doc ↔ table never linked | finale **federates** on the shared key (part #, code) |

---

## Architecture

*The full course-design treatment — graph models, the recommendation/audit graph, the finale steps —
lives in `WORKSHOP-PLAN.md`. Summarized here for build-env context.*

**Principle:** migrate only what passes the four-pains test (sync, performance, modeling, security);
federate the rest.

| Data | Home | Why |
|------|------|-----|
| Warehouse **rows** (vehicles, work orders, parts, …) | **BigQuery only** | high-churn, large, already modeled, sensitive — copying fails all four pains |
| Warehouse **metadata** (tables, columns, FKs) | **Neo4j**, via neocarta | low-churn schema, tiny, models *connections* not data, low-sensitivity — wins all four; this is the justified load |
| **Documents** (PDFs → trees/themes) | **Neo4j** | no system of record owns them; the graph is their first useful structure — "structuring unstructured data," not migrating structured data |
| **Recommendations** (the agent's decisions) | **Neo4j** | the reasoning trail *is* a graph; auditable |

**The finale federates.** A judgment tool (e.g. `what_fixed_this`) runs in three steps:
1. **Neo4j** — full-text the code → the sections that mention it → read candidate part numbers from
   that section text (grounding). Part numbers / codes are **text**, not nodes.
2. **BigQuery SQL** — for those parts, on same-model/engine vehicles with the code, count uses and comebacks
3. **Python** — join + rank

neocarta's connections graph is what lets the agent write step 2's SQL correctly (it reads the FK
join paths). The document tree/themes shapes power step 1's grounding.

**Security knob to name honestly:** neocarta can pull sample column values (`HAS_VALUE`). For AutoFix
these are benign (part numbers, models) and help routing — include them, but call out that they are
the dial a security-conscious team weighs (pain #4).

---

## Positioning vs Text2SQL / Databricks Genie

Stress-tested red-team/blue-team (2026-06-09):
`~/Documents/content-research-wiki/outputs/autorepair-thesis-stress-test.md`. **Read it before
making competitive claims in the lessons.** The headline: do **not** frame this as "Genie/Text2SQL
*can't*." In 2026 Databricks ships the Mosaic AI Agent Framework + managed MCP (AI Search, Genie,
SQL, UC Functions) that *can* orchestrate vector+SQL across the doc↔table boundary, and Genie takes
declarative joins + metric views for pinned deterministic paths. A "the tools can't" pitch gets
destroyed by a sharp attendee. Win on **trust, not capability**.

- **The problem half is bulletproof — cite independent benchmarks, not vendor numbers:**
  - **Falcon (arXiv 2510.24762, Oct 2025): 78.57% error rate on queries touching 4+ tables** — the
    exact shape of the finale join (`work_orders → vehicles → work_order_parts → parts`). The single
    strongest stat; used in M2 L1/L2 and M5 L1.
  - Spider 2.0 (ICLR'25): frontier models ~10–17% on *enterprise* Text2SQL (vs ~86% academic);
    agentic "lite" tops ~73%.
  - Weller et al. 2025: a single dense embedding *geometrically* cannot represent arbitrary
    connected sets — vector returns the wrong *shape* (backs the trees/themes half).
- **The graph's honest edge = determinism + auditability + one traversal**, vs. an orchestrated
  tool-chain that re-derives the join each query and is ~70–80% reliable. Modeled once, inspectable.
- **The cross-modal point is the real moat:** bulletin *applicability* is not a column — it is text
  the graph turns into a traversable edge. The counter to "just declare a metric view then": that is
  the same modeling work; the graph does it once *and* holds the unstructured side.
- Where this shows up in the course: M2 L1 "the tool guesses" NOTE + M2 L2 `path_query.py` payoff
  (deterministic path → SQL → live rows) + M5 L1 "but can a Databricks agent not orchestrate this?"
  NOTE.

### Positioning vs OSI / semantic-layer standards (for OSI-aware learners)

Some participants arrive with **OSI / dbt / Databricks Metric Views** in their heads and will ask
where the course fits. Handle it in **one framing**, then move on — do **not** teach the OSI spec
(that turns the course into a spec tutorial that chases revisions).

- **What OSI/semantic layers standardize:** the *meaning* layer — metrics, dimensions, synonyms.
  A commodity *interface*, not where our value lives.
- **What this course is about:** the *connections shape* (structure + join paths) and **agent grounding**
  on top of it — the layer OSI does **not** specify, and which works even on the **far more common
  warehouse that has no semantic layer at all**.
- **The one-liner for "but I already have OSI":** *"OSI carries the meaning; the graph is where
  cross-source reasoning and agent retrieval happen — including for the warehouses with no curated
  semantic layer. neocarta ingests OSI if you have it; the course is about the graph you build from it
  and beyond it."*
- **Principle (keeps us off the standards treadmill):** adopt the standard thinly at the boundary
  (ingest/transpile), innovate above it (graph, derivation, agent activation). Acknowledging OSI ≠
  teaching or chasing it.

---

## Module outline (2 hr)

*Authoritative module/lesson breakdown is in `WORKSHOP-PLAN.md`. Build-env summary:*

| M | Module | Shape | Mode | ~min |
|---|--------|-------|------|------|
| 1 | The Context Problem + Setup | — | talk + setup | 15 |
| 2 | **Connections** — neocarta over BigQuery | paths | hands-on (use tool, read its shape) | 25 |
| 3 | Navigate the Documents | trees | hands-on (build-from-spec) | 25 |
| 4 | Surface Themes | communities | hands-on (build-from-spec) | 25 |
| 5 | **Put It Together** — federated finale, THE RUN, decide & act | all (federated) | hands-on (build-from-spec) | 25 |
| 6 | Wrap Up — derive vs. federate, port the pattern | — | talk + quiz | 5 |
| opt | **General graph reasoning with neo4j-cli** | — | optional (in M4) | ~10 |

Setup (M1) connects the Codespace to **both BigQuery (read) and a Neo4j sandbox** and starts the parts
API — the sandbox starts **empty**. M2 loads the **connections** metadata graph
(`load/build_connections.py`); M3 then loads the **document graph** (`load/load_documents.py`, documents
only — the warehouse is never loaded into Neo4j) at the point the documents become the subject, and shows
it live in the sandbox. The two loaders write disjoint labels (`:Table`/`:Column` vs.
`:Library`/`:Folder`/`:Document`/`:Section`); `load_documents.py` scopes its wipe to the document half, so
running it in M3 leaves M2's connections graph intact.

---

## Pipeline (build env — this repo)

`tools/catalog.frozen.json` is the **single source of truth** for *both* halves, so corpus and warehouse
always agree. Two pipelines, both under `load/`:

- **Corpus (documents → Neo4j):** authored markdown in `corpus/<area>/<id>.md` (**183 docs**) →
  `tools/render_corpus.py` (markdown → PDFs, cross-references embedded as real PDF link annotations) →
  `load/parse_corpus.py` (headings → sections; link annotations → `LINKS_TO`; URLs → stub Documents) →
  `load/load_documents.py` (renamed from `load_graph.py`; **documents only** — wipes + loads the document
  graph: **183 docs / 985 sections / 1306 `LINKS_TO`**).
- **Warehouse (→ BigQuery, never Neo4j):** `tools/generate_warehouse.py` builds CSVs from the catalog
  (~1,700 vehicles / ~12.3k work_orders); loaded via `bigquery/setup.sh`.
- **Connections (neocarta → Neo4j):** `load/build_connections.py` (moved from `connections/`) reads the
  BigQuery schema → **6 tables / 5 REFERENCES**; exposed via the `connections` MCP server (`.mcp.json`).
- **Events:** `tools/generate_events.py` → `events/wo-2026-011{7,8,9}.json`.
- **Themes:** Leiden over `LINKS_TO` collapsed to Documents (no glue nodes) → ~**13 themes** by shared
  cross-references.

**Skill** (`.claude/skills/autofix-service-advisor/`): `SKILL.md` + `scripts/` (`outline.py`, `search.py`,
`themes.py` are build-from-spec in M3–4; `run_sql.py`, `bq.py`, `db.py`, `order_part.py`,
`write_recommendation.py` given). Complete reference impls in `solutions/scripts/` (incl. the M5
`what_fixed_this.py` / `recall_exposure.py` / `path_query.py`).

**Removed v1 dead code:** `load_graph.py`, `parse_pdfs.py`, `tools/warehouse_source.py`, `tools/data_def.py`,
`tools/generate_sources.py`, and the `data/` integrated-sandbox CSV dataset.

---

## Build state (snapshot — slow-changing; work items in issues)

| Piece | State |
|-------|-------|
| Shape-first version (trees, themes, skill, Codespace) | **shipped** `v1.47.12` |
| Domain-agnostic document model + 183-doc corpus + docs-only pipeline | **done / shipped** |
| BigQuery warehouse (expanded) + DDL/access (`bigquery/`) | **done / shipped** |
| M2 Connections (neocarta `load/build_connections.py` + `connections` MCP) | **done / shipped** |
| Federated finale (`what_fixed_this`/`recall_exposure` over Neo4j+BigQuery) | **done**, validated end-to-end |
| Module reorder + M1/M5/M6 reframe + optional neo4j-cli | **done**, QA green |
| Integrated-sandbox path removed (`data/` deleted; Codespace+BigQuery only) | **done** |
| Content aligned & verified end-to-end (full Codespace runthrough) | **green** (2026-06; see WORKSHOP-PLAN verification) |
| BigQuery read auth in Codespace (shared SA key) | **remaining** — the one infra item gating self-serve |
| Artwork, prod release, org move, reviews, `:status: draft → active` | **deferred** |

---

## Work tracking

All actionable work is in GitHub issues prefixed **`lakehouse-workshop:`** (label
`lakehouse-workshop`) on **`neo4j-graphacademy/courses`**:

→ https://github.com/neo4j-graphacademy/courses/labels/lakehouse-workshop

This doc holds the durable plan; the issues hold the to-dos. Do not re-add a checklist here.
