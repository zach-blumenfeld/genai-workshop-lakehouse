# AutoFix warehouse in BigQuery

The warehouse half of the lakehouse lives here — **in BigQuery, never migrated
into Neo4j** (see `docs/COURSE-PLAN.md` → Architecture). neocarta reads its
*metadata* (the foreign-key join paths) to build the connections shape; the
finale federates against the live rows. This folder provisions it.


## What gets created

Dataset `autofix_service` with six tables and their key constraints:

```
vehicles(vin PK)
dtc_codes(code PK)
procedures(procedure_id PK)
parts(part_number PK, superseded_by — column, not FK*)
work_orders(wo_id PK, vin FK→vehicles, dtc_code FK→dtc_codes, procedure_id FK→procedures)
work_order_parts(wo_id+part_number PK, FK→work_orders, FK→parts)
```

\* `superseded_by` is a self-reference (part → its replacement); BigQuery rejects
foreign keys that point at their own table, so it stays a plain column. The agent
reads supersession via SQL, and the parts API still enforces it with a 409.

The PK/FK constraints are **NOT ENFORCED** — BigQuery does not validate them,
but they appear in `INFORMATION_SCHEMA`, which is what neocarta turns into the
`Column-[:REFERENCES]->Column` graph. No declared keys → no join paths → no
connections shape. That's why they matter.

## Provision it (you, the admin — run once)

Prereqs: `gcloud` SDK installed + authed (`gcloud auth login`), a GCP project
with BigQuery + billing enabled.

```bash
GCP_PROJECT_ID=<your-project> ./bigquery/setup.sh
# or a clean reprovision:
GCP_PROJECT_ID=<your-project> ./bigquery/setup.sh --fresh
```

It creates the dataset, runs `schema.sql`, loads the CSVs from
`sources/warehouse/`, and grants public read. Verify the keys neocarta will read:

```bash
bq query --use_legacy_sql=false \
  "SELECT table_name, column_name, constraint_name
   FROM \`<your-project>.autofix_service\`.INFORMATION_SCHEMA.KEY_COLUMN_USAGE
   ORDER BY table_name"
```

You should see the six foreign keys above.

## Access model

**You:** full admin (project owner) — nothing to grant.

**Participants:** read-only. `setup.sh` runs:

```sql
GRANT `roles/bigquery.dataViewer` ON SCHEMA `<project>.autofix_service`
  TO 'allAuthenticatedUsers';
```

- `allAuthenticatedUsers` = any Google-authenticated caller can read (no per-person grant). Swap to `allUsers` via `GRANTEE=allUsers ./bigquery/setup.sh` for truly anonymous read.
- This grants **read on the data + metadata**. It does **not** grant write, and participants cannot see other datasets in your project.

### The billing nuance (decide before the workshop)

BigQuery bills **query compute to the caller's project**, not the dataset
owner's. So `dataViewer` lets a participant *see* the data, but to *run a query*
(neocarta's metadata read, or the finale's federated SQL) they need a GCP
project of their own to bill against — friction for a hosted workshop.

The dataset is ~150 rows, so query cost is effectively zero. Recommended
participant path (wired into the Codespace in **#579**):

- **Shared read-only service account.** Create an SA in your project with
  `roles/bigquery.dataViewer` (on the dataset) + `roles/bigquery.jobUser` (to
  run queries, billed to your project). Ship its key in the Codespace, like the
  Anthropic key. Tiny dataset = negligible cost; revoke after the event.
- Alternative: participants `gcloud auth` with their own project (no shared key,
  but every participant needs a GCP project).

`dataViewer` to `allAuthenticatedUsers` is still the right dataset grant either
way — the SA decision is only about *who pays for the query*.

## Files

- `schema.sql` — DDL (tables + PK/FK), `${PROJECT}`/`${DATASET}` placeholders
- `setup.sh` — admin provisioning script (create, load, grant)
