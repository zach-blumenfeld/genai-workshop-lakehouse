"""BigQuery helper for the federated finale.

The warehouse rows live in BigQuery (never migrated). These tools query them
live and join the result against the Neo4j document graph. Project + dataset
come from .env (GCP_PROJECT_ID, BIGQUERY_DATASET_ID).

Auth: paste the workshop read-only key from the slides into .env as
BIGQUERY_SA_KEY_B64 (one line). If it is not set, your own gcloud login is used.
"""

import base64
import json
import os

from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv(override=True)

PROJECT = os.environ["GCP_PROJECT_ID"]
DATASET = os.environ.get("BIGQUERY_DATASET_ID", "autofix_service")


def bq_client(project):
    """A BigQuery client: the workshop read-only service account if
    BIGQUERY_SA_KEY_B64 is set, otherwise your own gcloud credentials."""
    b64 = os.environ.get("BIGQUERY_SA_KEY_B64")
    if b64:
        from google.oauth2 import service_account
        info = json.loads(base64.b64decode(b64))
        creds = service_account.Credentials.from_service_account_info(info)
        return bigquery.Client(project=project, credentials=creds)
    return bigquery.Client(project=project)


_client = None


def _bq():
    global _client
    if _client is None:
        _client = bq_client(PROJECT)
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
