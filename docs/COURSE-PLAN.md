# Course Plan — AI on Your Lakehouse: Context Comes in Shapes, Not Queries

**Source of truth.** Update this doc when goals, architecture, or outline change.
Actionable work lives in **GitHub issues prefixed `lakehouse-workshop:`** (label
`lakehouse-workshop`), not in this file — see [Work tracking](#work-tracking).

- **Course content:** `neo4j-graphacademy/courses` → `asciidoc/courses/workshop-lakehouse/` (live, `:status: draft`, prod URL serves it)
- **Build environment:** `zach-blumenfeld/genai-workshop-lakehouse` (this repo — Codespace, pipeline, skill, specs)
- **Status:** shape-first version shipped (`v1.47.12`); **neocarta/BigQuery restructure built on branch `lakehouse-connections-m2` (federated finale, runnable) - pending review/merge**

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
- Data model matured to the **ki-style containment graph**: `Library → Folder → Document → Section`,
  single `HAS` type, hierarchical URIs, `NEXT_SECTION` reading order, content with `uri:` child
  pointers, `LINKS_TO` split into citations vs. derived shared-key links
- **Shape-first became the explicit method**: read the spec (`docs/outline-format.md`,
  `docs/theme-format.md`) → derive the graph reasoning → build. Added a **search** shape-tool
  (hierarchical fulltext + agent-side semantic expansion) not in the baseline
- **Louvain → Leiden** (conductance-backed cohesion words, `gamma` granularity dial)

### This restructure — neocarta + federation (in progress)

- **Module reorder:** connections/paths moves from **last → first**. New order:
  connections → trees → themes → finale → wrap
- **neocarta added** as the connections tool, over **BigQuery** (Databricks deferred until its
  connector lands)
- **Architecture reversal — no structured-data migration.** The baseline said *"load the Delta
  warehouse via Data Importer, merge on the shared key."* That is **removed.** Warehouse rows stay
  in BigQuery; only neocarta's **metadata graph** migrates; the finale **federates** (live BigQuery
  SQL + Neo4j grounding). See [Architecture](#architecture).
- **New second axis to the thesis:** not just *what* shape, but *where it lives* — derive vs. federate
- **neo4j-cli optional section** for general graph reasoning; **6 modules + optional**, not 5

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

**Principle:** migrate only what passes the four-pains test (sync, performance, modeling, security);
federate the rest.

| Data | Home | Why |
|------|------|-----|
| Warehouse **rows** (vehicles, work orders, parts, …) | **BigQuery only** | high-churn, large, already modeled, sensitive — copying fails all four pains |
| Warehouse **metadata** (tables, columns, FKs) | **Neo4j**, via neocarta | low-churn schema, tiny, models *connections* not data, low-sensitivity — wins all four; this is the justified load |
| **Documents** (PDFs → trees/themes) | **Neo4j** | no system of record owns them; the graph is their first useful structure — "structuring unstructured data," not migrating structured data |
| **Recommendations** (the agent's decisions) | **Neo4j** | the reasoning trail *is* a graph; auditable |

**The finale federates.** A judgment tool (e.g. `what_fixed_this`) runs in three steps:
1. **Neo4j** — which documents cover the code, which parts do they reference → candidate parts + grounding sections
2. **BigQuery SQL** — for those parts, on same-model/engine vehicles with the code, count uses and comebacks
3. **Python** — join + rank

neocarta's connections graph is what lets the agent write step 2's SQL correctly (it reads the FK
join paths). Shape 1 powers the finale.

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

---

## Module outline (2 hr, target)

| M | Module | Shape | Mode | ~min |
|---|--------|-------|------|------|
| 1 | The Context Problem + Setup | — | talk + setup | 15 |
| 2 | **Connections** — neocarta over BigQuery | paths | hands-on (use tool, read its shape) | 25 |
| 3 | Navigate the Documents | trees | hands-on (build-from-spec) | 25 |
| 4 | Surface Themes | communities | hands-on (build-from-spec) | 25 |
| 5 | **Put It Together** — judgment tools, THE RUN, decide & act | all (federated) | hands-on (build-from-spec) | 25 |
| 6 | Wrap Up — derive vs. federate, port the pattern | — | talk + quiz | 5 |
| opt | **General graph reasoning with neo4j-cli** | — | optional | ~10 |

Setup (M1) connects the Codespace to **both BigQuery (read) and a Neo4j sandbox**. The graph
import in M3 is **documents only**.

---

## Build state (snapshot — slow-changing; work items in issues)

| Piece | State |
|-------|-------|
| Shape-first version (trees, themes, skill, Codespace) | **shipped** `v1.47.12` |
| BigQuery warehouse + DDL/access (`bigquery/`) | **done**, pushed (env repo) |
| M2 Connections (neocarta `build_connections.py` + agentic `connections` MCP) | **done**, on branch + env repo |
| Docs-only pipeline (warehouse load removed) | **done** |
| Federated finale (`what_fixed_this`/`recall_exposure` over Neo4j+BigQuery) | **done**, validated |
| Module reorder + M1/M5/M6 reframe + optional neo4j-cli | **done**, QA green |
| BigQuery read auth in Codespace (shared SA key) | **remaining** — #581 |
| PR, prod release, org move, artwork, reviews, `:status: active` | **deferred** |

---

## Work tracking

All actionable work is in GitHub issues prefixed **`lakehouse-workshop:`** (label
`lakehouse-workshop`) on **`neo4j-graphacademy/courses`**:

→ https://github.com/neo4j-graphacademy/courses/labels/lakehouse-workshop

This doc holds the durable plan; the issues hold the to-dos. Do not re-add a checklist here.
