"""BigQuery helper for the federated finale.

The warehouse rows live in BigQuery (never migrated). These tools query them
live and join the result against the Neo4j document graph. Project + dataset
come from .env (GCP_PROJECT_ID, BIGQUERY_DATASET_ID); auth is the read access
provided for the workshop (a service account, or your own gcloud login).
"""

import os

from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv(override=True)

PROJECT = os.environ["GCP_PROJECT_ID"]
DATASET = os.environ.get("BIGQUERY_DATASET_ID", "autofix_service")

_client = None


def _bq():
    global _client
    if _client is None:
        _client = bigquery.Client(project=PROJECT)
    return _client


def table(name):
    """Fully-qualified, backtick-quoted table reference."""
    return f"`{PROJECT}.{DATASET}.{name}`"


def _params(d):
    out = []
    for k, v in d.items():
        if isinstance(v, list):
            out.append(bigquery.ArrayQueryParameter(k, "STRING", v))
        else:
            out.append(bigquery.ScalarQueryParameter(k, "STRING", v))
    return out


def bq_query(sql, params=None):
    """Run a parameterized BigQuery SQL query; return a list of dict rows."""
    cfg = bigquery.QueryJobConfig(query_parameters=_params(params or {}))
    return [dict(r) for r in _bq().query(sql, job_config=cfg).result()]
