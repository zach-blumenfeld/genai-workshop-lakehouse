"""Upload the AutoFix PDF library into a Unity Catalog Volume.

Creates a managed Volume `{CATALOG}.{SCHEMA}.{VOLUME}` and uploads every PDF
under sources/pdfs/<area>/*.pdf, preserving the area/ prefix. These are the
PDFs that AI Search indexes (the document half of the AutoFix data on
Databricks). Idempotent: CREATE VOLUME IF NOT EXISTS + overwrite uploads.

Env (a .env is loaded if present; same vars as load_databricks.py):
  DATABRICKS_SERVER_HOSTNAME   e.g. dbc-xxxx.cloud.databricks.com  (no https://)
  DATABRICKS_HTTP_PATH         e.g. /sql/1.0/warehouses/abc123
  DATABRICKS_TOKEN             a PAT (dapi...) or OAuth token
  DATABRICKS_CATALOG           default: autofix
  DATABRICKS_SCHEMA            default: autofix_service
  DATABRICKS_VOLUME            default: pdfs

Run:  python databricks/upload_pdfs.py
"""

import glob
import os
from pathlib import Path

from dotenv import load_dotenv
from databricks import sql
from databricks.sdk import WorkspaceClient

load_dotenv(override=True)

HOST = os.environ["DATABRICKS_SERVER_HOSTNAME"]
HTTP_PATH = os.environ["DATABRICKS_HTTP_PATH"]
TOKEN = os.environ["DATABRICKS_TOKEN"]
CATALOG = os.environ.get("DATABRICKS_CATALOG", "autofix")
SCHEMA = os.environ.get("DATABRICKS_SCHEMA", "autofix_service")
VOLUME = os.environ.get("DATABRICKS_VOLUME", "pdfs")

PDF_DIR = Path(__file__).resolve().parent.parent / "sources" / "pdfs"
VOL_PATH = f"/Volumes/{CATALOG}/{SCHEMA}/{VOLUME}"


def main():
    # 1) create the Volume (SQL warehouse connection)
    with sql.connect(server_hostname=HOST, http_path=HTTP_PATH, access_token=TOKEN) as conn:
        with conn.cursor() as cur:
            cur.execute(f"CREATE VOLUME IF NOT EXISTS `{CATALOG}`.`{SCHEMA}`.`{VOLUME}`")
    print(f"Volume ready: {VOL_PATH}")

    # 2) upload every PDF via the Files API (SDK)
    w = WorkspaceClient(host=f"https://{HOST}", token=TOKEN)
    files = sorted(glob.glob(str(PDF_DIR / "**" / "*.pdf"), recursive=True))
    print(f"Uploading {len(files)} PDFs from {PDF_DIR} ...")
    for i, f in enumerate(files, 1):
        rel = os.path.relpath(f, PDF_DIR)  # e.g. bulletins/tsb-20-501.pdf
        with open(f, "rb") as fh:
            w.files.upload(f"{VOL_PATH}/{rel}", fh, overwrite=True)
        if i % 50 == 0:
            print(f"  {i}/{len(files)}")
    print(f"Done: uploaded {len(files)} PDFs to {VOL_PATH}/<area>/")


if __name__ == "__main__":
    main()
