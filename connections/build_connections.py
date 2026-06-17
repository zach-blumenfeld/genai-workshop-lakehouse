"""Build the connections graph — the warehouse's metadata, never its rows.

Runs neocarta's BigQuery schema connector against the AutoFix warehouse and
writes the metadata graph (Database -> Schema -> Table -> Column, with
Column-[:REFERENCES]->Column from the foreign keys) into your Neo4j sandbox.

This is the connections shape: the join-path map an agent reads to route a
question to the right tables and write correct SQL. The warehouse *rows* stay
in BigQuery — only this metadata crosses over (see docs/COURSE-PLAN.md ->
Architecture for why that passes the four-pains test).

Connection + dataset come from .env:
  NEO4J_URI / NEO4J_USERNAME / NEO4J_PASSWORD / NEO4J_DATABASE
  GCP_PROJECT_ID        (billing project; the shared workshop project)
  BIGQUERY_DATASET_ID   (defaults to autofix_service)
  BIGQUERY_SA_KEY_B64   (the workshop read-only key from the slides; if unset,
                         your own gcloud login is used)

Run:  python connections/build_connections.py
"""

import base64
import json
import os

from dotenv import load_dotenv
from google.cloud import bigquery
from neo4j import GraphDatabase

from neocarta.connectors.bigquery import BigQuerySchemaConnector

load_dotenv(override=True)

PROJECT = os.environ["GCP_PROJECT_ID"]
DATASET = os.environ.get("BIGQUERY_DATASET_ID", "autofix_service")


def bq_client(project):
    """Workshop read-only service account if BIGQUERY_SA_KEY_B64 is set,
    otherwise your own gcloud credentials."""
    b64 = os.environ.get("BIGQUERY_SA_KEY_B64")
    if b64:
        from google.oauth2 import service_account
        info = json.loads(base64.b64decode(b64))
        creds = service_account.Credentials.from_service_account_info(info)
        return bigquery.Client(project=project, credentials=creds)
    return bigquery.Client(project=project)


def main():
    driver = GraphDatabase.driver(
        os.environ["NEO4J_URI"],
        auth=(os.environ["NEO4J_USERNAME"], os.environ["NEO4J_PASSWORD"]),
    )
    database = os.environ.get("NEO4J_DATABASE", "neo4j")
    client = bq_client(PROJECT)

    print(f"Reading {PROJECT}.{DATASET} metadata -> Neo4j ({database})...")
    # Schema only — no embeddings (the FK graph is the join map; the warehouse
    # has six tables, small enough that the agent reads the whole shape).
    BigQuerySchemaConnector(
        client=client,
        project_id=PROJECT,
        neo4j_driver=driver,
        database_name=database,
    ).ingest(dataset_id=DATASET)

    with driver.session(database=database) as s:
        refs = s.run("MATCH (:Column)-[r:REFERENCES]->(:Column) RETURN count(r) AS n").single()["n"]
        tables = s.run("MATCH (t:Table) RETURN count(t) AS n").single()["n"]
    driver.close()
    print(f"Connections graph ready: {tables} tables, {refs} REFERENCES (join paths).")
    print("Your agent reads this through the connections MCP (get_full_metadata_schema).")


if __name__ == "__main__":
    main()
