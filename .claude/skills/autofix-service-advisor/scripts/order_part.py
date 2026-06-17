"""SOLUTION: Order a part through the AutoFix parts API.

Usage: python solutions/scripts/order_part.py WO-2026-0117 IC-2042-B [qty]

A 409 response means the part is superseded - the API names the
replacement. Surface it; do not retry automatically.
"""

import json
import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv(override=True)  # .env is the source of truth, even over exported vars

wo_id, part_number = sys.argv[1], sys.argv[2]
qty = int(sys.argv[3]) if len(sys.argv) > 3 else 1

response = requests.post(
    f"{os.environ.get('PARTS_API_URL', 'http://localhost:8800')}/orders",
    headers={"X-API-Key": os.environ.get("PARTS_API_KEY", "")},
    json={"wo_id": wo_id, "part_number": part_number, "qty": qty},
    timeout=10,
)
print(f"HTTP {response.status_code}")
print(json.dumps(response.json(), indent=2))
