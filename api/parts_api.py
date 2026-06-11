"""AutoFix parts ordering API (mock dealer-management system).

Stands in for the external system a service-advisor agent orders parts
through. Run it in a second terminal:

    .venv/bin/uvicorn api.parts_api:app --port 8800

Authentication: X-API-Key header must match PARTS_API_KEY from .env.

Behavior worth knowing:
- POST /orders rejects parts that are superseded (HTTP 409) and names the
  replacement - exactly what a real parts system does, and exactly the
  feedback an agent must handle.
- Orders are held in memory; GET /orders shows everything placed this session.
"""

import csv
import itertools
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

load_dotenv()

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_KEY = os.environ.get("PARTS_API_KEY", "autofix-workshop-key")

app = FastAPI(title="AutoFix Parts API")

# The parts catalog is the warehouse export - same vocabulary as the graph.
CATALOG = {}
with open(os.path.join(ROOT, "sources", "warehouse", "parts.csv"), newline="") as f:
    for row in csv.DictReader(f):
        CATALOG[row["part_number"]] = row

ORDERS = []
_ids = itertools.count(1)


class OrderRequest(BaseModel):
    wo_id: str
    part_number: str
    qty: int = 1


def check_key(x_api_key):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing X-API-Key")


@app.post("/orders")
def place_order(order: OrderRequest, x_api_key: str = Header(default="")):
    check_key(x_api_key)
    part = CATALOG.get(order.part_number)
    if part is None:
        raise HTTPException(status_code=404, detail=f"Unknown part {order.part_number}")
    if part["superseded_by"]:
        raise HTTPException(
            status_code=409,
            detail=(
                f"Part {order.part_number} is superseded by {part['superseded_by']} "
                f"and can no longer be ordered. Order {part['superseded_by']} instead."
            ),
        )
    record = {
        "order_id": f"PO-{next(_ids):04d}",
        "wo_id": order.wo_id,
        "part_number": order.part_number,
        "part_name": part["name"],
        "qty": order.qty,
        "status": "submitted",
    }
    ORDERS.append(record)
    return record


@app.get("/orders")
def list_orders(x_api_key: str = Header(default="")):
    check_key(x_api_key)
    return ORDERS
