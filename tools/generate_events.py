"""Regenerate the incoming work-order events against the current warehouse.

Three events, each with a deliberate finale outcome, using REAL vins from the
regenerated fleet (sources/warehouse/vehicles.csv):

- 0117 REPAIR   : a misfire (P0301) on a Falcon 2.0T - strong evidence, the
                  revised coil IC-2042-B is the comeback-free fix.
- 0118 ESCALATE : a code on a model+engine the warehouse has NO repair history
                  for - the finale finds no evidence and must escalate.
- 0119 NO-CODE  : brake judder with no DTC - grounding comes from the complaint's
                  theme (brakes), not a code.

Run: .venv/bin/python tools/generate_events.py
"""

import csv
import json
import os
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WH = os.path.join(ROOT, "sources", "warehouse")
EVENTS = os.path.join(ROOT, "events")


def rows(name):
    with open(os.path.join(WH, f"{name}.csv")) as f:
        return list(csv.DictReader(f))


veh = rows("vehicles")
wo = rows("work_orders")
wop = rows("work_order_parts")
by_vin = {v["vin"]: v for v in veh}

wo_vin = {w["wo_id"]: w["vin"] for w in wo}
applied_by_vin = {}  # vin -> set(part_number) it has already received
for r in wop:
    applied_by_vin.setdefault(wo_vin[r["wo_id"]], set()).add(r["part_number"])

# (model, engine) combos that have at least one work order per code
combos_for_code = defaultdict(set)
for w in wo:
    v = by_vin.get(w["vin"])
    if v:
        combos_for_code[w["dtc_code"]].add((v["model"], v["engine"]))
all_combos = {(v["model"], v["engine"]) for v in veh}


def first_vin(model, engine):
    return next(v["vin"] for v in veh if v["model"] == model and v["engine"] == engine)


# --- 0117 REPAIR: a Falcon 2.0T that has NOT yet had the coil recall remedy
# IC-2042-B, so recall_exposure reliably flags the open coil recall to bundle. ---
repair_vin = next(
    (v["vin"] for v in veh if v["model"] == "Falcon" and v["engine"] == "2.0T"
     and "IC-2042-B" not in applied_by_vin.get(v["vin"], set())),
    first_vin("Falcon", "2.0T"),
)

# --- 0118 ESCALATE: pick U0121 on a (model,engine) with NO U0121 history ---
escalate_code = "U0121"
no_history = sorted(all_combos - combos_for_code[escalate_code])
esc_model, esc_engine = no_history[0]
escalate_vin = first_vin(esc_model, esc_engine)

# --- 0119 NO-CODE: brake judder, any vehicle (theme grounding, no code) ---
nocode_vin = first_vin("Marlin EV", next(v["engine"] for v in veh if v["model"] == "Marlin EV"))

events = [
    {
        "file": "wo-2026-0117.json",
        "wo_id": "WO-2026-0117", "vin": repair_vin, "opened": "2026-06-15", "odometer": 52340,
        "complaint": "Check engine light flashing, rough idle at stops, customer reports loss of power on hills",
        "dtc_code": "P0301",
    },
    {
        "file": "wo-2026-0118.json",
        "wo_id": "WO-2026-0118", "vin": escalate_vin, "opened": "2026-06-15", "odometer": 18920,
        "complaint": "ABS warning light on intermittently, no other symptoms",
        "dtc_code": escalate_code,
    },
    {
        "file": "wo-2026-0119.json",
        "wo_id": "WO-2026-0119", "vin": nocode_vin, "opened": "2026-06-16", "odometer": 41250,
        "complaint": "Steering wheel shakes when braking from highway speed, started a few weeks after front pads were done elsewhere",
        "dtc_code": "",
    },
]

os.makedirs(EVENTS, exist_ok=True)
for e in events:
    fname = e.pop("file")
    with open(os.path.join(EVENTS, fname), "w") as f:
        json.dump(e, f, indent=2)
        f.write("\n")
    v = by_vin[e["vin"]]
    print(f"  {fname}: {e['vin']} ({v['model']} {v['engine']}) code={e['dtc_code'] or '(none)'}")

print(f"\nescalate check: {esc_model} {esc_engine} has {len(combos_for_code[escalate_code])} "
      f"model+engine combos with {escalate_code} history; this one has none -> escalate.")
