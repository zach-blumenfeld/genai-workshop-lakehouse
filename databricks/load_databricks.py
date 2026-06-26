"""Create the AutoFix warehouse in Databricks Unity Catalog and load it.

Mirrors bigquery/schema.sql: six Delta tables with informational PRIMARY KEY /
FOREIGN KEY constraints (Unity Catalog surfaces these in information_schema -
the join paths the connections shape reads). Data comes from sources/warehouse/*.csv.

Idempotent: CREATE TABLE IF NOT EXISTS + INSERT OVERWRITE, so re-running resets
the rows without dropping the schema.

Env (a .env is loaded if present):
  DATABRICKS_SERVER_HOSTNAME   e.g. dbc-xxxx.cloud.databricks.com   (no https://)
  DATABRICKS_HTTP_PATH         e.g. /sql/1.0/warehouses/abc123
  DATABRICKS_TOKEN             a PAT (dapi...) or OAuth token
  DATABRICKS_CATALOG           default: autofix
  DATABRICKS_SCHEMA            default: autofix_service

Run:  python databricks/load_databricks.py
"""

import csv
import os
from pathlib import Path

from dotenv import load_dotenv
from databricks import sql

load_dotenv(override=True)

HOST = os.environ["DATABRICKS_SERVER_HOSTNAME"]
HTTP_PATH = os.environ["DATABRICKS_HTTP_PATH"]
TOKEN = os.environ["DATABRICKS_TOKEN"]
CATALOG = os.environ.get("DATABRICKS_CATALOG", "autofix")
SCHEMA = os.environ.get("DATABRICKS_SCHEMA", "autofix_service")
FQ = f"`{CATALOG}`.`{SCHEMA}`"  # backticked so hyphenated catalog names work


def t(name):
    """Backtick-quoted fully-qualified table name."""
    return f"{FQ}.`{name}`"
SRC = Path(__file__).resolve().parent.parent / "sources" / "warehouse"

# column name -> type tag, in CSV order, per table
TABLES = {
    "vehicles": [("vin", "str"), ("make", "str"), ("model", "str"), ("year", "int"), ("engine", "str")],
    "dtc_codes": [("code", "str"), ("description", "str")],
    "procedures": [("procedure_id", "str"), ("name", "str"), ("labor_hours", "float")],
    "parts": [("part_number", "str"), ("name", "str"), ("superseded_by", "str")],
    "work_orders": [("wo_id", "str"), ("vin", "str"), ("opened", "date"), ("odometer", "int"),
                    ("complaint", "str"), ("dtc_code", "str"), ("procedure_id", "str"), ("comeback", "bool")],
    "work_order_parts": [("wo_id", "str"), ("part_number", "str"), ("qty", "int")],
}

# DDL — order matters: a table must exist before another FKs to it.
DDL = [
    f"CREATE SCHEMA IF NOT EXISTS {FQ}",
    f"""CREATE TABLE IF NOT EXISTS {FQ}.vehicles (
        vin STRING NOT NULL, make STRING, model STRING, year INT, engine STRING,
        CONSTRAINT pk_vehicles PRIMARY KEY (vin)) COMMENT 'One row per serviced vehicle.'""",
    f"""CREATE TABLE IF NOT EXISTS {FQ}.dtc_codes (
        code STRING NOT NULL, description STRING,
        CONSTRAINT pk_dtc_codes PRIMARY KEY (code)) COMMENT 'OBD-II diagnostic trouble code reference.'""",
    f"""CREATE TABLE IF NOT EXISTS {FQ}.procedures (
        procedure_id STRING NOT NULL, name STRING, labor_hours DOUBLE,
        CONSTRAINT pk_procedures PRIMARY KEY (procedure_id)) COMMENT 'Labor procedures.'""",
    f"""CREATE TABLE IF NOT EXISTS {FQ}.parts (
        part_number STRING NOT NULL, name STRING, superseded_by STRING,
        CONSTRAINT pk_parts PRIMARY KEY (part_number)) COMMENT 'Parts catalog; superseded_by points to the replacement.'""",
    f"""CREATE TABLE IF NOT EXISTS {FQ}.work_orders (
        wo_id STRING NOT NULL, vin STRING, opened DATE, odometer INT, complaint STRING,
        dtc_code STRING, procedure_id STRING, comeback BOOLEAN,
        CONSTRAINT pk_work_orders PRIMARY KEY (wo_id),
        CONSTRAINT fk_wo_vehicle FOREIGN KEY (vin) REFERENCES {FQ}.vehicles(vin),
        CONSTRAINT fk_wo_dtc FOREIGN KEY (dtc_code) REFERENCES {FQ}.dtc_codes(code),
        CONSTRAINT fk_wo_procedure FOREIGN KEY (procedure_id) REFERENCES {FQ}.procedures(procedure_id))
        COMMENT 'A repair visit; comeback = true means the vehicle returned with the same problem.'""",
    f"""CREATE TABLE IF NOT EXISTS {FQ}.work_order_parts (
        wo_id STRING NOT NULL, part_number STRING NOT NULL, qty INT,
        CONSTRAINT pk_work_order_parts PRIMARY KEY (wo_id, part_number),
        CONSTRAINT fk_wop_workorder FOREIGN KEY (wo_id) REFERENCES {FQ}.work_orders(wo_id),
        CONSTRAINT fk_wop_part FOREIGN KEY (part_number) REFERENCES {FQ}.parts(part_number))
        COMMENT 'Parts replaced on a work order (bridge: work_orders <-> parts).'""",
]


def lit(value, tag):
    """Format a CSV string as a SQL literal for its column type."""
    if value is None or value == "":
        return "NULL"
    if tag == "str":
        return "'" + value.replace("'", "''") + "'"
    if tag == "int":
        return str(int(value))
    if tag == "float":
        return str(float(value))
    if tag == "bool":
        return "TRUE" if str(value).strip().lower() in ("true", "1", "t", "yes") else "FALSE"
    if tag == "date":
        return f"DATE'{value}'"
    raise ValueError(tag)


def load_rows(cur, table, cols):
    rows = list(csv.DictReader(open(SRC / f"{table}.csv")))
    names = [c for c, _ in cols]
    values = ",\n".join(
        "(" + ", ".join(lit(r[c], t) for c, t in cols) + ")" for r in rows
    )
    cur.execute(f"INSERT OVERWRITE {FQ}.{table} ({', '.join(names)}) VALUES\n{values}")
    return len(rows)


def main():
    print(f"Connecting to {HOST} -> {FQ}")
    with sql.connect(server_hostname=HOST, http_path=HTTP_PATH, access_token=TOKEN) as conn:
        with conn.cursor() as cur:
            for stmt in DDL:
                cur.execute(stmt)
            print("Schema ready (6 tables, PK/FK constraints).")
            total = 0
            for table, cols in TABLES.items():
                n = load_rows(cur, table, cols)
                total += n
                print(f"  loaded {table}: {n} rows")
    print(f"Done: {FQ} loaded ({total} rows).")


if __name__ == "__main__":
    main()
