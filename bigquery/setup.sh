#!/usr/bin/env bash
# Provision the AutoFix warehouse in BigQuery — admin run-once.
#
# Creates the dataset, the six tables (with PK/FK constraints), loads the
# sample rows from sources/warehouse/, and grants public read access.
# YOU (the project owner) run this; participants only ever get read access.
#
# Prereqs: gcloud SDK installed and authed (`gcloud auth login`), a GCP project
# with BigQuery enabled, and billing on that project.
#
# Usage:
#   GCP_PROJECT_ID=my-project ./bigquery/setup.sh
#   GCP_PROJECT_ID=my-project DATASET=autofix_service LOCATION=US ./bigquery/setup.sh --fresh
#
# Flags:
#   --fresh   drop and recreate the dataset first (destructive; clean reprovision)
set -euo pipefail

: "${GCP_PROJECT_ID:?set GCP_PROJECT_ID to your GCP project}"
DATASET="${DATASET:-autofix_service}"
LOCATION="${LOCATION:-US}"
# Truly public read = allUsers; Google-authenticated read = allAuthenticatedUsers.
GRANTEE="${GRANTEE:-allAuthenticatedUsers}"

HERE="$(cd "$(dirname "$0")" && pwd)"
WAREHOUSE="$(cd "$HERE/../sources/warehouse" && pwd)"

echo "Project:  $GCP_PROJECT_ID"
echo "Dataset:  $DATASET ($LOCATION)"
echo "Grantee:  $GRANTEE (roles/bigquery.dataViewer)"
echo

if [[ "${1:-}" == "--fresh" ]]; then
  echo "--- dropping dataset $DATASET (--fresh)"
  bq --project_id="$GCP_PROJECT_ID" rm -r -f -d "$DATASET" 2>/dev/null || true
fi

echo "--- creating dataset"
bq --project_id="$GCP_PROJECT_ID" --location="$LOCATION" mk -d \
  --description "AutoFix Group service warehouse (workshop sample)" "$DATASET" 2>/dev/null \
  || echo "    (dataset exists)"

echo "--- creating tables + foreign keys"
sed -e "s/\${PROJECT}/$GCP_PROJECT_ID/g" -e "s/\${DATASET}/$DATASET/g" "$HERE/schema.sql" \
  | bq --project_id="$GCP_PROJECT_ID" query --use_legacy_sql=false

echo "--- loading rows"
# Do NOT use `bq load --replace`: it overwrites the table SCHEMA (dropping the
# PK/FK constraints the DDL just created). TRUNCATE clears rows but keeps the
# schema + constraints; then append the CSV into the existing schema.
for t in vehicles dtc_codes procedures parts work_orders work_order_parts; do
  echo "    $t"
  bq --project_id="$GCP_PROJECT_ID" query --use_legacy_sql=false \
    "TRUNCATE TABLE \`$GCP_PROJECT_ID.$DATASET.$t\`" >/dev/null
  bq --project_id="$GCP_PROJECT_ID" load \
    --source_format=CSV --skip_leading_rows=1 --null_marker='' \
    "$DATASET.$t" "$WAREHOUSE/$t.csv"
done

echo "--- granting public read (dataset-level dataViewer)"
bq --project_id="$GCP_PROJECT_ID" query --use_legacy_sql=false \
  "GRANT \`roles/bigquery.dataViewer\` ON SCHEMA \`$GCP_PROJECT_ID.$DATASET\` TO '$GRANTEE'"

echo
echo "Done. Verify the join-path graph neocarta will read:"
echo "  bq --project_id=$GCP_PROJECT_ID query --use_legacy_sql=false \\"
echo "    \"SELECT * FROM \\\`$GCP_PROJECT_ID.$DATASET\\\`.INFORMATION_SCHEMA.KEY_COLUMN_USAGE\""
echo
echo "Participants connect with GCP_PROJECT_ID=$GCP_PROJECT_ID, BIGQUERY_DATASET_ID=$DATASET."
echo "NOTE: read access lets anyone SEE the data, but running a query bills the"
echo "caller's own project. See bigquery/README.md -> Participant access for the"
echo "shared read-only service-account pattern (wired into the Codespace in #579)."
