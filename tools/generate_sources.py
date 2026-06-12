"""Generate the AutoFix lakehouse sources from the canonical dataset.

Produces:
- sources/pdfs/{manuals,bulletins,recalls}/<DOC-ID>.pdf  - the technical library
- sources/warehouse/*.csv                                - Delta table exports

The PDFs are the system of record for the document half: numbered headings,
real citation sentences, no synthetic markers. The load pipeline parses them
(load/parse_pdfs.py); the GCS bucket mirrors this folder layout, so the
prefixes (manuals/ bulletins/ recalls/) become :Folder nodes.

Run: .venv/bin/python tools/generate_sources.py
"""

import csv
import os
import shutil
import sys

from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data_def

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_DIR = os.path.join(ROOT, "sources", "pdfs")
WH_DIR = os.path.join(ROOT, "sources", "warehouse")

FOLDER_BY_TYPE = {"Manual": "manuals", "Bulletin": "bulletins", "RecallNotice": "recalls"}

PAGE_W, PAGE_H = LETTER
MARGIN = 54
LINE_H = 14
WRAP = 92


def wrap(text, width=WRAP):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        lines.append(cur)
    return lines


class Pdf:
    def __init__(self, path):
        self.c = canvas.Canvas(path, pagesize=LETTER)
        self.y = PAGE_H - MARGIN

    def line(self, text, font="Helvetica", size=10):
        if self.y < MARGIN:
            self.c.showPage()
            self.y = PAGE_H - MARGIN
        self.c.setFont(font, size)
        self.c.drawString(MARGIN, self.y, text)
        self.y -= LINE_H

    def blank(self):
        self.y -= LINE_H / 2

    def save(self):
        self.c.save()


def section_tree(doc_id):
    """Yield (section, depth, number) in document order."""
    rows = [s for s in data_def.sections if s[1] == doc_id]
    tops = sorted([s for s in rows if not s[2]], key=lambda s: s[3])
    for i, top in enumerate(tops, 1):
        yield top, 0, str(i)
        children = sorted([s for s in rows if s[2] == top[0]], key=lambda s: s[3])
        for j, child in enumerate(children, 1):
            yield child, 1, f"{i}.{j}"


def write_pdf(doc):
    doc_id, doc_type, title, model, published = doc
    folder = os.path.join(PDF_DIR, FOLDER_BY_TYPE[doc_type])
    os.makedirs(folder, exist_ok=True)
    pdf = Pdf(os.path.join(folder, f"{doc_id}.pdf"))
    pdf.line("AutoFix Group Technical Library", "Helvetica-Oblique", 9)
    pdf.blank()
    pdf.line(title, "Helvetica-Bold", 14)
    pdf.blank()
    # Metadata block - parsed by load/parse_pdfs.py
    pdf.line(f"Document: {doc_id}")
    pdf.line(f"Type: {doc_type}")
    pdf.line(f"Model: {model}")
    pdf.line(f"Published: {published}")
    pdf.blank()
    for section, depth, number in section_tree(doc_id):
        _, _, _, _, s_title, s_text = section
        indent = "  " * depth
        pdf.blank()
        pdf.line(f"{indent}{number} {s_title}", "Helvetica-Bold", 11)
        for ln in wrap(s_text):
            pdf.line(f"{indent}{ln}")
    pdf.save()


def write_csv(name, header, rows):
    with open(os.path.join(WH_DIR, name), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"warehouse/{name}: {len(rows)} rows")


def main():
    if os.path.isdir(PDF_DIR):
        shutil.rmtree(PDF_DIR)
    os.makedirs(WH_DIR, exist_ok=True)
    for doc in data_def.documents:
        write_pdf(doc)
        print(f"pdfs/{FOLDER_BY_TYPE[doc[1]]}/{doc[0]}.pdf")
    write_csv("parts.csv", ["part_number", "name", "superseded_by"], data_def.parts)
    write_csv("dtc_codes.csv", ["code", "description"], data_def.dtc_codes)
    write_csv("procedures.csv", ["procedure_id", "name", "labor_hours"], data_def.procedures)
    write_csv("vehicles.csv", ["vin", "make", "model", "year", "engine"], data_def.vehicles)
    write_csv(
        "work_orders.csv",
        ["wo_id", "vin", "opened", "odometer", "complaint", "dtc_code", "procedure_id", "comeback"],
        [(w, v, o, od, c, d, p, str(cb).lower()) for w, v, o, od, c, d, p, cb in data_def.work_orders],
    )
    write_csv("work_order_parts.csv", ["wo_id", "part_number", "qty"], data_def.work_order_parts)


if __name__ == "__main__":
    main()
