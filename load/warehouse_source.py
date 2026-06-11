"""Warehouse source adapters.

Every adapter yields plain dict rows for the six autofix.service.* tables:
parts, dtc_codes, procedures, vehicles, work_orders, work_order_parts.

CsvSource reads the exports in sources/warehouse/.
DatabricksSource reads the live Unity Catalog tables - same row shapes, so
swapping sources changes nothing downstream.

Select with WAREHOUSE_SOURCE=csv|databricks (default csv).
"""

import csv
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TABLES = ["parts", "dtc_codes", "procedures", "vehicles", "work_orders", "work_order_parts"]


class CsvSource:
    """Reads the CSV exports in sources/warehouse/."""

    def __init__(self, folder=None):
        self.folder = folder or os.path.join(ROOT, "sources", "warehouse")

    def rows(self, table):
        with open(os.path.join(self.folder, f"{table}.csv"), newline="") as f:
            yield from csv.DictReader(f)


class DatabricksSource:
    """Reads the live Delta tables under Unity Catalog.

    Requires: pip install databricks-sql-connector, and the environment
    variables DATABRICKS_SERVER_HOSTNAME, DATABRICKS_HTTP_PATH,
    DATABRICKS_TOKEN. Catalog/schema default to autofix.service.
    """

    def __init__(self, catalog="autofix", schema="service"):
        from databricks import sql  # imported lazily - optional dependency

        self.conn = sql.connect(
            server_hostname=os.environ["DATABRICKS_SERVER_HOSTNAME"],
            http_path=os.environ["DATABRICKS_HTTP_PATH"],
            access_token=os.environ["DATABRICKS_TOKEN"],
        )
        self.catalog, self.schema = catalog, schema

    # Delta table names match the CSV table names one-to-one. The CSV column
    # headers are the contract; the SELECT aliases keep them identical.
    def rows(self, table):
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT * FROM {self.catalog}.{self.schema}.{table}")
            columns = [d[0] for d in cur.description]
            for row in cur.fetchall():
                yield dict(zip(columns, [("" if v is None else str(v)) for v in row]))


def get_source():
    kind = os.environ.get("WAREHOUSE_SOURCE", "csv").lower()
    if kind == "databricks":
        return DatabricksSource()
    return CsvSource()
