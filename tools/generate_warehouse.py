"""Generate the AutoFix warehouse CSVs from the frozen catalog + the corpus.

Reference tables (parts, dtc_codes, procedures) come straight from
tools/catalog.frozen.json. The fleet (vehicles) and repair history
(work_orders, work_order_parts) are synthesized so the M5 finale's evidence
ranking works:

- Which parts fix which code is derived from the CORPUS: parts and codes
  co-mentioned in the same section are associated (keeps warehouse and docs
  consistent, and handles cross-system fixes like a misfire code -> coil part).
- Superseded parts (parts.superseded_by set) carry a high comeback rate; their
  replacements carry a low one -> "what fixed this" prefers the revised part.

Outputs sources/warehouse/*.csv (columns match bigquery/schema.sql).
Reload BigQuery with `bigquery/setup.sh --fresh` (needs gcloud owner auth).

Run: .venv/bin/python tools/generate_warehouse.py
"""

import csv
import json
import os
import random
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "load"))
from parse_corpus import parse_all  # noqa: E402

WH = os.path.join(ROOT, "sources", "warehouse")
rng = random.Random(7)

catalog = json.load(open(os.path.join(ROOT, "tools", "catalog.frozen.json")))
parts = catalog["parts"]
codes = catalog["dtcCodes"]
procs = catalog["procedures"]
models = catalog["models"]

part_sys = {p["partNumber"]: p["system"] for p in parts}
superseded = {p["partNumber"]: p["supersededBy"] for p in parts if p["supersededBy"]}
code_sys = {c["code"]: c["system"] for c in codes}
proc_by_sys = defaultdict(list)
for p in procs:
    proc_by_sys[p["system"]].append(p["procedureId"])

# ---- 1. code -> fix parts/procedure, by corpus section co-occurrence ----
_, _, _, sections, _ = parse_all()
part_nums = sorted((p["partNumber"] for p in parts), key=len, reverse=True)
code_list = [c["code"] for c in codes]
proc_ids = [p["procedureId"] for p in procs]

code_parts = defaultdict(Counter)
code_procs = defaultdict(Counter)
for s in sections:
    body = s["content"]
    present_codes = [c for c in code_list if re.search(r"\b" + re.escape(c) + r"\b", body)]
    if not present_codes:
        continue
    present_parts = [pn for pn in part_nums if pn in body]
    present_procs = [pr for pr in proc_ids if pr in body]
    for c in present_codes:
        for pn in present_parts:
            code_parts[c][pn] += 1
        for pr in present_procs:
            code_procs[c][pr] += 1


def fix_parts_for(code):
    cc = code_parts[code]
    if cc:
        return [pn for pn, _ in cc.most_common(3)]
    sysname = code_sys.get(code)
    same = [p["partNumber"] for p in parts if p["system"] == sysname]
    return same[:2] if same else [parts[0]["partNumber"]]


def fix_proc_for(code, fps):
    cc = code_procs[code]
    if cc:
        return cc.most_common(1)[0][0]
    for pn in fps:
        if proc_by_sys[part_sys[pn]]:
            return proc_by_sys[part_sys[pn]][0]
    return procs[0]["procedureId"]


# ---- 2. fleet: vehicles per model x engine ----
# Large fleet so each vehicle's service history is sparse (a few parts, not most
# of the catalog) - otherwise every car looks like it had every recall remedy and
# recall_exposure never finds anything. Per-(model,engine,code) evidence for the
# finale is an aggregate over the whole fleet, so it is unaffected by fleet size.
YEARS = [2019, 2020, 2021, 2022, 2023]
VEH_PER_COMBO = 100
vehicles = []
fleet = defaultdict(list)  # (model, engine) -> [vin]
for m in models:
    abbr = re.sub(r"[^A-Z0-9]", "", m["model"].upper())[:3] or "VEH"
    for engine in m["engines"]:
        eabbr = re.sub(r"[^A-Z0-9]", "", engine.upper())[:3]
        for n in range(VEH_PER_COMBO):
            year = rng.choice(YEARS)
            vin = f"{abbr}{eabbr}{year}{len(vehicles):04d}"
            vehicles.append((vin, m["make"], m["model"], year, engine))
            fleet[(m["model"], engine)].append(vin)


# ---- 3. work orders + work_order_parts ----
def models_for_code(code):
    """Deterministic 3-5 models per code; always include the first two for continuity."""
    base = [models[0]["model"], models[1]["model"]]
    others = [m["model"] for m in models[2:]]
    h = sum(ord(ch) for ch in code)
    rng2 = random.Random(h)
    rng2.shuffle(others)
    return list(dict.fromkeys(base + others[: 2 + (h % 3)]))


work_orders = []
wo_parts = []
wo_seq = 0
for code in code_list:
    fps = fix_parts_for(code)
    proc = fix_proc_for(code, fps)
    primary = fps[0]
    # supersession story: if the fix family has an original w/ a replacement
    orig = next((pn for pn in fps if pn in superseded), None)
    repl = superseded.get(orig) if orig else None
    secondary = [pn for pn in fps[1:] if pn not in (orig, repl)][:1]  # e.g. spark plugs alongside coil
    desc = next((c["description"] for c in codes if c["code"] == code), code)

    for model_name in models_for_code(code):
        engines = next((m["engines"] for m in models if m["model"] == model_name), [])
        for engine in engines:
            vins = fleet.get((model_name, engine), [])
            if not vins:
                continue
            M = rng.randint(26, 36)
            for j in range(M):
                wo_seq += 1
                wo_id = f"WO-{wo_seq:06d}"
                vin = rng.choice(vins)
                year_open = rng.choice(["2023", "2024", "2025"])
                opened = f"{year_open}-{rng.randint(1,12):02d}-{rng.randint(1,28):02d}"
                odo = rng.randint(20000, 140000)
                if orig:
                    # earlier ~40% used the original (unreliable), rest the revised part
                    use_orig = j < max(3, int(M * 0.4))
                    used = ([orig] if use_orig else [repl]) + secondary
                    comeback = (rng.random() < 0.55) if use_orig else (rng.random() < 0.03)
                else:
                    used = fps[:2]
                    comeback = rng.random() < 0.07
                work_orders.append((wo_id, vin, opened, odo, f"{desc}", code, proc, str(comeback).lower()))
                for pn in used:
                    wo_parts.append((wo_id, pn, 1 if not pn.startswith("SP-") else 1))


# ---- 4. write CSVs ----
def write_csv(name, header, rows):
    with open(os.path.join(WH, name), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"  warehouse/{name}: {len(rows)} rows")


def labor_hours(pid):
    return round(0.3 + (sum(ord(c) for c in pid) % 23) / 10.0, 1)


os.makedirs(WH, exist_ok=True)
print("Writing warehouse CSVs from catalog.frozen.json + corpus associations:")
write_csv("parts.csv", ["part_number", "name", "superseded_by"],
          [(p["partNumber"], p["name"], p["supersededBy"]) for p in parts])
write_csv("dtc_codes.csv", ["code", "description"], [(c["code"], c["description"]) for c in codes])
write_csv("procedures.csv", ["procedure_id", "name", "labor_hours"],
          [(p["procedureId"], p["name"], labor_hours(p["procedureId"])) for p in procs])
write_csv("vehicles.csv", ["vin", "make", "model", "year", "engine"], vehicles)
write_csv("work_orders.csv",
          ["wo_id", "vin", "opened", "odometer", "complaint", "dtc_code", "procedure_id", "comeback"],
          work_orders)
write_csv("work_order_parts.csv", ["wo_id", "part_number", "qty"], wo_parts)
print(f"Done: {len(vehicles)} vehicles, {len(work_orders)} work orders, {len(wo_parts)} work_order_parts, "
      f"{len(code_parts)} codes associated to parts from the corpus.")
