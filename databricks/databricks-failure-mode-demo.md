# The Databricks Failure Mode — Demo Runbook & Positioning Brief

*For the "AI on Your Lakehouse: Context Comes in Shapes, Not Queries" workshop (AutoFix Group).*
*Authored 2026-06-25. All product statuses verified by web search on that date — see [Sources](#5-sources).*

---

## 1. TL;DR / positioning

A modern Databricks agent **can** answer "ask questions across PDFs + a warehouse." The 2026 stack —
Mosaic AI Agent Framework / Agent Bricks orchestrating **AI Search** (vector) over the PDFs and **Genie**
(text-to-SQL, now backed by **Metric Views** and the new **Genie Ontology**) over the tables — is a real,
well-engineered way to wire that up. **So do not pitch "Databricks can't."** A sharp attendee will (correctly)
break that pitch in thirty seconds.

Win on **trust, not capability.** The canonical question — *"What actually fixed code P0301 on cars like this
Falcon?"* — fails not because any single tool is incapable, but because the answer requires (a) grounding in a
**document** (which bulletin/recall applies), (b) a **4-table warehouse join** to count real repair outcomes, and
(c) a **cross-modal join** on a key — the part number `IC-2042-A` and the applicability "Falcon 2.0T" — that is
**text inside a PDF, not a column anywhere.** The Databricks stack stitches this with two *probabilistic* retrievers
(similarity search) bridged by an LLM that writes *non-deterministic* multi-table SQL, and there is **no single
inspectable traversal** you can audit. Independent benchmarks put error on 4+-table Text2SQL at ~78.6% and frontier
LLMs at ~10–21% on enterprise Text2SQL; a 2025 DeepMind result shows a single embedding vector *geometrically cannot*
return arbitrary connected result sets. The graph finale answers the same question with **one deterministic,
inspectable path** over a model that names the doc↔row relationships explicitly. That is the contrast to demonstrate.

---

## 2. The modern Databricks approach (as you'd actually build it in 2026)

This is the steel-man. Build it at its best.

### 2.1 The orchestration layer — Mosaic AI Agent Framework / Agent Bricks

A tool-calling **retrieval agent** authored against the MLflow `ResponsesAgent` interface
(`mlflow>=3.1`, `databricks-agents>=1.1`), or assembled no-code as an **Agent Bricks** *Knowledge Assistant*
(GA 2026-01-27) coordinated by a **Supervisor Agent** (GA 2026-02-10). The agent reaches data through
**Databricks managed MCP servers** (**Public Preview** as of 2026-06-23):

| MCP server | URL pattern | Role in our query |
|---|---|---|
| **AI Search** (formerly Vector Search) | `/api/2.0/mcp/ai-search/{catalog}/{schema}/{index}` | Retrieve the bulletins/recalls relevant to "P0301 misfire" |
| **Genie Space** | `/api/2.0/mcp/genie/{genie_space_id}` | NL→SQL over the work-orders warehouse |
| **Databricks SQL** | `/api/2.0/mcp/sql` | Direct SQL execution |
| **Unity Catalog Functions** | `/api/2.0/mcp/functions/{catalog}/{schema}/{fn}` | Custom registered tools |

The LLM **sequences** these tool calls: query AI Search for documents, query Genie for the join, fuse the two in its
own reasoning. This is the orchestration the canonical query needs, and Databricks built exactly the plumbing for it.

### 2.2 The document half — AI Search (Vector Search) over the PDFs

- Parse PDFs with **`ai_parse_document`** (SQL, **GA** 2026-04-16) → chunk with **`ai_prep_search`** (Beta) →
  embed with a Foundation-Model embedding endpoint (e.g. `databricks-gte-large-en`, 1024-dim) → index in a
  **Delta Sync** AI Search index (**GA**).
- Retrieval is `similarity_search` / `vector_search()` with `query_type` ∈ `ANN | HYBRID | FULL_TEXT`
  (hybrid = vector + keyword via Reciprocal Rank Fusion, **GA**).
- **This half is similarity-based by construction.** It returns the *top-k most similar chunks*, not "the set of
  documents whose stated applicability covers this VIN." That distinction is the seed of the failure mode (§4).

### 2.3 The table half — Genie + Metric Views + Genie Ontology

This is where the "ton of ontology and semantic-layer stuff" the user flagged actually lives. Here is what shipped,
precisely:

- **Unity Catalog Metric Views** — the semantic layer for **metrics + dimensions**. **GA 2026-04-02** (UI authoring &
  materialization in Public Preview; core being open-sourced into Apache Spark, SPARK-54119). You declare measures and
  dimensions once, and **declarative joins in YAML** (`joins:` with `source` + `on:` predicate) supporting star/snowflake/
  multi-level/one-to-many over PK/FK constraints (`RELY`). This is genuinely deterministic **where the relationship is
  pre-modeled over structured tables.**
- **Genie** (text-to-SQL "spaces"), next-gen announced 2026-04-26; **Genie One / Genie Agents / Genie Ontology**
  headlined at Data + AI Summit 2026 (2026-06-16). Genie uses **trusted assets** (certified example SQL + SQL functions)
  to return verified answers; Databricks explicitly says it "chose **not** to build another error-prone text-to-SQL
  interface" and leans on pre-vetted assets + the Ontology. Databricks' own benchmark: **84.5% correct on first attempt**
  across 28 real-world questions (vs 52.4% for "the strongest general-purpose coding agent").
- **Genie Ontology** — **Public Preview**, 2026-06-16; Ali Ghodsi called it one of the Summit's most important
  announcements. It is a **self-improving knowledge graph** that *auto-extracts* knowledge snippets from tables, queries,
  dashboards, pipelines and 50+ connected apps, ranks them with **OntoRank** (a PageRank-style authority/usage/freshness
  score), and routes the highest-authority **context** to Genie so it queries trusted SQL instead of guessing.
- Adjacent DAIS-2026 items: **Glossary** (business concepts/taxonomy — "Preview coming soon," i.e. announced not shipped);
  **Domains** (Public Preview); **Multimodal/`FILE` type** governing unstructured files (Beta).

**Built at its best, the canonical answer would be:** Agent Framework → AI Search MCP for the bulletin → Genie MCP
(grounded by a Metric View / Ontology) for the work-order join → LLM fuses them. Represent it that way to the room. Then
show where it breaks.

---

## 3. Reusable runbook (run this on your Databricks account)

Goal: stand up the steel-man pipeline on the AutoFix sample, run the P0301 question several times, and capture the
failures in §4. The repo already has the warehouse loader; you add the docs index + Genie + agent.

### 3.0 Prereqs

- A Databricks workspace with Unity Catalog, a SQL warehouse, **AI Search** enabled, and **managed MCP** (Public Preview).
- Local repo `/Users/zach/dev/genai-workshop-lakehouse` with `sources/warehouse/*.csv` and `sources/pdfs/**/*.pdf`.
- Set the loader env (a `.env` is auto-loaded): `DATABRICKS_SERVER_HOSTNAME`, `DATABRICKS_HTTP_PATH`,
  `DATABRICKS_TOKEN`, `DATABRICKS_CATALOG` (default `autofix`), `DATABRICKS_SCHEMA` (default `autofix_service`).

### 3.1 Load the warehouse (six Delta tables, PK/FK constraints)

The repo ships the loader — use it as-is:

```bash
python databricks/load_databricks.py
```

It creates `vehicles, dtc_codes, procedures, parts, work_orders, work_order_parts` with **informational PK/FK
constraints** (these are exactly the join paths a Metric View / Genie reads from `information_schema`). The join the
canonical query needs is `work_orders → vehicles` (VIN), `work_orders → work_order_parts → parts` (part_number),
plus `work_orders.dtc_code`. **Four tables.** Note `parts.superseded_by` (e.g. `IC-2042-A → IC-2042-B`) and
`work_orders.comeback` (the vehicle came back with the same problem — the real signal of whether a fix *actually worked*).

### 3.2 Land the PDFs in a UC Volume and build the AI Search index

In a Databricks notebook (outline; exact SQL/SDK names per §5 docs):

```python
# 1. Create a Volume and upload sources/pdfs/** into it
#    (databricks fs cp -r sources/pdfs dbfs:/Volumes/autofix/autofix_service/pdfs)
```

```sql
-- 2. Parse + chunk the PDFs entirely in SQL (Document Intelligence path)
CREATE OR REPLACE TABLE autofix.autofix_service.doc_chunks AS
SELECT path,
       ai_parse_document(content) AS parsed     -- GA 2026-04-16
FROM   READ_FILES('/Volumes/autofix/autofix_service/pdfs/**', format => 'binaryFile');
-- then ai_prep_search(...) to explode parsed -> search-ready chunks (Beta)
```

```python
# 3. Create a Delta Sync AI Search index over the chunk table
from databricks.vector_search.client import VectorSearchClient   # legacy alias still works
vsc = VectorSearchClient()
vsc.create_delta_sync_index(
    endpoint_name="autofix_vs",
    index_name="autofix.autofix_service.doc_index",
    source_table_name="autofix.autofix_service.doc_chunks",
    pipeline_type="TRIGGERED",
    primary_key="chunk_id",
    embedding_source_column="chunk_text",
    embedding_model_endpoint_name="databricks-gte-large-en",
)
```

### 3.3 Stand up a Genie space (or a Metric View) over the tables

- Create a **Genie space** scoped to the six `autofix_service` tables. Add **instructions** describing the join
  paths and a couple of **trusted-asset** example queries (this is the honest, best-effort config — give it every
  advantage).
- Optionally model a **Metric View** (`measures: timesUsed = COUNT(DISTINCT wo_id)`, `comebacks = COUNT_IF(comeback)`;
  `joins:` `work_orders→vehicles`, `work_orders→work_order_parts→parts`) so the *declared* metric is deterministic.
  **Note what you cannot put in it:** there is no `bulletin`, no `applicability`, no `dtc→part` mapping — those live
  only in PDF prose. The Metric View can only join columns that already exist.

### 3.4 Wire the agent (Agent Framework or Agent Bricks)

Point a `ResponsesAgent` (or an Agent Bricks Knowledge Assistant + Supervisor) at **both** MCP servers:

```python
from databricks_mcp import DatabricksMCPClient
from databricks.sdk import WorkspaceClient
ws = WorkspaceClient()
search = DatabricksMCPClient(server_url=f"{host}/api/2.0/mcp/ai-search/autofix/autofix_service/doc_index", workspace_client=ws)
genie  = DatabricksMCPClient(server_url=f"{host}/api/2.0/mcp/genie/{genie_space_id}", workspace_client=ws)
# Register both tool sets with the LLM; let it sequence: search PDFs -> query Genie -> fuse.
```

Test interactively in **AI Playground** before scripting.

### 3.5 Run the canonical question (and variants) — several times each

Ask the agent, verbatim, **5–10 times in fresh sessions** (this repetition *is* the experiment):

1. **Canonical:** *"What actually fixed code P0301 on cars like this Falcon (VIN FAL20T20200047, 2.0T)?"*
2. **Variant A (applicability):** *"Which bulletin or recall applies to a 2020 Falcon 2.0T with P0301, and which part is the current fix?"* — forces the textual-applicability + supersession step.
3. **Variant B (outcomes join):** *"For Falcon 2.0T cars with P0301, which replaced part had the fewest comebacks?"* — forces the 4-table join with the `comeback` measure.

Ground truth (from the sample): the applicable documents are **TSB-20-501** ("Falcon 2.0T: cylinder misfire from cracked
ignition coil," P0300/P0301) and recall **RC-2021-01**; the fix is coil **IC-2042-A superseded by IC-2042-B** (+ inspect
plug SP-1108); the outcome ranking comes from joining `work_orders→vehicles→work_order_parts→parts` and counting
`comeback`. The graph finale produces exactly this with one traversal.

---

## 4. What to capture as the failure

Screenshot / log these. Each is an honest **trust** failure, not a "tool can't" claim.

1. **Non-deterministic / wrong multi-table joins (run-to-run variance).** Run questions 1 and 3 several times. Capture
   cases where the generated SQL changes between runs, drops the `work_order_parts` bridge, mis-joins on VIN vs model+engine,
   double-counts on the many-to-many, or silently returns a different "best part." *Anchor:* Falcon (arXiv 2510.24762,
   2025-10-23) reports **78.57% error on Text2SQL queries touching ≥4 tables**; Spider 2.0 (ICLR'25) baselines are
   **10.1% (GPT-4o) / 17.1% (o1-preview)** on full enterprise Text2SQL (agentic "lite" tops out ~73%). Even Databricks'
   own best-case Genie number is **84.5% first-attempt** — i.e. ~1 in 6 wrong, with no flag telling you which one.
   *The Metric View narrows this only for the join you pre-modeled — it does not make the LLM's column/filter choices
   deterministic, and it can't model the join that isn't in the schema (step 3).*

2. **Can't reliably tie the bulletin's textual applicability to the right vehicles (the cross-modal gap).** The bulletin
   says it affects **"Falcon 2.0T"** and the fix is part **IC-2042-A → IC-2042-B** — both are **prose in a PDF**, not
   columns. AI Search returns *similar chunks*, so capture: (a) it surfaces a near-miss bulletin (e.g. a different
   misfire TSB) ranked above the right one; (b) it returns the chunk but the agent never connects "Falcon 2.0T applicability"
   to the VIN's `make/model/engine` row, or never carries `IC-2042-A` into the SQL `WHERE part_number = …`; (c) it misses the
   **supersession** (recommends the discontinued `IC-2042-A`). *Anchor:* Weller, Boratko, Naim & Lee, *On the Theoretical
   Limitations of Embedding-Based Retrieval* (arXiv 2508.21038, 2025-08-28; v2 2026-03-12) — the number of distinct top-k
   result sets a single embedding can return is **bounded by its dimension**, independent of model power: a single vector
   geometrically returns the wrong *shape*. (Flag the nuance: a 2026 follow-up, arXiv 2603.29519, argues dimensionality
   *alone* doesn't explain real failures — domain-shift / relevance-misalignment dominate; either way single-vector
   retrieval is the wrong instrument for "the connected set.")

3. **No single auditable traversal.** The "answer" is assembled across two probabilistic retrievers and an LLM's private
   chain-of-thought. Capture the MLflow trace and ask: *can a service manager point at one inspectable path from "VIN +
   P0301" → "this bulletin applies" → "this part" → "these outcomes"?* No — the doc↔table link exists only transiently
   inside the model's reasoning, and reruns produce different traces. There is nothing to certify, diff, or sign off.

**The contrast (the graph finale):** the same question resolves to **one deterministic Cypher/federation traversal** over
a model that makes the doc↔row relationships *explicit and inspectable* — full-text-find the section that mentions `P0301`,
read the part numbers from that section's text, traverse the named connections to `work_orders → vehicles →
work_order_parts → parts`, rank by `comeback` ascending. Same path every run; every hop is a relationship a human
authored, not a similarity score; the whole traversal is one auditable artifact. **That is the trust gap to land.**

### Honest assessment: do the 2026 ontology features close this?

**No — and be precise about why, because this is the load-bearing claim.** Metric Views (GA) and Genie Ontology (Public
Preview) are real and they *do* pin declared metrics/joins (deterministic *where pre-modeled*) and route ranked, governed
context to the agent. But:

- **(i) Same modeling work, narrower scope.** They only pin joins over **table-like assets** that already expose a tabular
  schema — Metric Views docs explicitly exclude unstructured/document sources. You still have to model everything, and you
  can't model the relationship that doesn't exist as columns.
- **(ii) They do not cover the cross-modal step.** A bulletin's *applicability* ("affects 2019–2021 Falcon 2.0T") and its
  *part numbers* are **unstructured text**, not a metric or dimension. None of the shipped/previewed features lets you
  declare a typed entity-relationship join between a **text mention inside a PDF** and a **structured table row** on that
  shared key. Genie Ontology *auto-extracts and ranks* snippets — it is a retrieval/authority layer, not a user-defined ER
  graph; it does not expose "entity X in this PDF = row in this table on text key Y."
- **(iii) The doc-retrieval half is still similarity-based.** Ontology context-ranking sits *on top of* the same vector
  retrieval; it improves which structured context Genie trusts, not the geometry of finding the connected set in §4.2.

So the new stack moves the *structured-side* determinism forward and improves context governance — genuinely useful — but
the specific capability the workshop is about (a queryable, inspectable graph linking PDF text to table rows on a shared
text key, traversed the same way every time) **remains the gap.** That is the honest, attendee-proof version of the pitch.

---

## 5. Sources

*All accessed 2026-06-25. Statuses (GA / Public Preview / Beta) are as observed on that date.*

**Agent stack & MCP**
- Mosaic AI Agent Framework — build GenAI apps: https://docs.databricks.com/aws/en/generative-ai/agent-framework/build-genai-apps · author-agent · deploy-agent. Announcement (2024-07-02): https://www.databricks.com/blog/announcing-mosaic-ai-agent-framework-and-agent-evaluation
- Agent Bricks (Beta, 2025-06-11): https://www.databricks.com/blog/introducing-agent-bricks · Knowledge Assistant **GA 2026-01-27**: https://www.databricks.com/blog/agent-bricks-knowledge-assistant-now-generally-available-turning-enterprise-knowledge-answers · Supervisor Agent **GA 2026-02-10**: https://www.databricks.com/blog/agent-bricks-supervisor-agent-now-ga-orchestrate-enterprise-agents · KA docs: https://docs.databricks.com/aws/en/generative-ai/agent-bricks/knowledge-assistant
- Managed MCP servers — **Public Preview**, docs updated 2026-06-23: https://docs.databricks.com/aws/en/generative-ai/mcp/managed-mcp · overview: https://docs.databricks.com/aws/en/generative-ai/mcp/ · announcement (2025-06-18): https://www.databricks.com/blog/announcing-managed-mcp-servers-unity-catalog-and-mosaic-ai-integration

**AI Search / Vector Search & PDF parsing**
- AI Search (Vector Search), **GA**: https://docs.databricks.com/aws/en/vector-search/vector-search · create: https://docs.databricks.com/aws/en/vector-search/create-vector-search · query: https://docs.databricks.com/aws/en/ai-search/query-ai-search
- Foundation Model embedding endpoints (`databricks-gte-large-en`, `databricks-bge-large-en`), page updated 2026-06-11: https://docs.databricks.com/aws/en/machine-learning/foundation-model-apis/supported-models
- `ai_parse_document` **GA 2026-04-16**: https://docs.databricks.com/aws/en/sql/language-manual/functions/ai_parse_document · blog: https://www.databricks.com/blog/pdfs-production-announcing-state-art-document-intelligence-databricks
- Hybrid search **GA** (2024-08-26): https://www.databricks.com/blog/announcing-hybrid-search-general-availability-mosaic-ai-vector-search

**Semantic layer / ontology (the "ton of ontology stuff")**
- Unity Catalog Metric Views / Business Semantics **GA 2026-04-02** (UI & materialization Public Preview; SPARK-54119): https://www.databricks.com/blog/redefining-semantics-data-layer-future-bi-and-ai · docs (updated 2026-06-12): https://docs.databricks.com/aws/en/business-semantics/metric-views · joins/modeling: https://docs.databricks.com/aws/en/business-semantics/metric-views/basic-modeling
- Next-gen Genie (2026-04-26): https://www.databricks.com/blog/next-generation-databricks-genie · **Genie One / Genie Ontology / Genie Agents** (2026-06-16; Genie Ontology = Public Preview): https://www.databricks.com/blog/introducing-genie-one-genie-ontology-and-genie-agents · secondary (Atlan, 2026-06-19): https://atlan.com/know/ai-agent/databricks/genie-ontology/
- Genie best practices / trusted assets: https://docs.databricks.com/aws/en/genie/best-practices · tune quality: https://docs.databricks.com/aws/en/genie/tune-quality · AI/BI + Genie release notes 2026 (84.5% benchmark): https://docs.databricks.com/aws/en/ai-bi/release-notes/2026
- What's new in Unity Catalog at DAIS 2026 (Glossary "Preview coming soon", Domains, Multimodal `FILE` Beta): https://www.databricks.com/blog/whats-new-unity-catalog-data-ai-summit-2026

**Independent benchmarks (the reliability anchors)**
- **Falcon** — *Falcon: A Comprehensive Chinese Text-to-SQL Benchmark for Enterprise-Grade Evaluation*, Luo et al., arXiv 2510.24762 (2025-10-23). **78.57% error on ≥4-table queries** (≥4-table accuracy 21.43%; best model DeepSeek-R1 45.2% overall): https://arxiv.org/abs/2510.24762
- **Spider 2.0** — *Evaluating Language Models on Real-World Enterprise Text-to-SQL Workflows*, Lei et al., arXiv 2411.07763, ICLR 2025 (Oral). Full enterprise baselines **GPT-4o 10.1% / o1-preview 17.1%**; paper's agent 21.3%; leaderboard Spider 2.0-Lite top ~73.13% (2026-06): https://arxiv.org/abs/2411.07763 · https://spider2-sql.github.io/
- **Weller et al.** — *On the Theoretical Limitations of Embedding-Based Retrieval*, Weller, Boratko, Naim & Lee (Google DeepMind/JHU), arXiv 2508.21038 (2025-08-28; v2 2026-03-12). Number of returnable top-k sets is **bounded by embedding dimension**; introduces the LIMIT dataset: https://arxiv.org/abs/2508.21038
- *Nuance/rebuttal* — *On Strengths and Limitations of Single-Vector Embeddings*, Archish S et al. (MSR India), arXiv 2603.29519 (2026-03-31): argues dimensionality alone doesn't explain failures ((2k+1)-dim suffices for top-k); single-vector finetuning causes catastrophic forgetting while multi-vector stays robust: https://arxiv.org/abs/2603.29519

**Local repo references**
- Warehouse loader: `/Users/zach/dev/genai-workshop-lakehouse/databricks/load_databricks.py` (six Delta tables + PK/FK constraints)
- Ground-truth docs: `corpus/bulletins/tsb-20-501.md`, `corpus/recalls/rc-2021-01.md` (Falcon 2.0T / P0300+P0301 / IC-2042-A→IC-2042-B / SP-1108)
- Graph-finale spec: `.claude/skills/autofix-service-advisor/SKILL.md` (the one-traversal contrast)

> **Flagged uncertainties:** (1) Mosaic AI Agent Framework shows no explicit "GA" wording on any page — GA-by-presentation, not confirmed. (2) Vector Search has been renamed **AI Search** (SDK `databricks-ai-search`; legacy `databricks-vectorsearch` / `VectorSearchClient` still work as aliases) — older tutorials use the old names. (3) `ai_prep_search` chunking and full-text-only indexes are **Beta**. (4) Genie Ontology's "Public Preview" status rests partly on a single secondary source (Atlan, 2026-06-19); the Databricks blog carries no explicit badge.
