"""Parse the AutoFix PDF library into documents, sections, and references.

Reads every PDF in sources/pdfs/ and produces plain dicts:

- documents: {id, doc_type, title, model, published}
- sections:  {id, doc_id, parent_id, seq, title, text}
- refs:      {section_id, ref_type: PART|CODE, ref_value}

Part numbers are recognised against the parts catalog (the warehouse is the
vocabulary - extraction with a known catalog is far more reliable than a bare
regex). Diagnostic trouble codes match the standard OBD-II pattern.

Swap point: replace iter_pdf_paths() to read from cloud storage instead of
the local sources/pdfs/ folder.
"""

import os
import re
from pypdf import PdfReader

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_DIR = os.path.join(ROOT, "sources", "pdfs")

HEADING = re.compile(r"^\s*(\d+(?:\.\d+)?)\s+(.+?)\s+\[Ref:\s*(\S+)\]\s*$")
META = re.compile(r"^(Document|Type|Model|Published):\s*(.+)$")
DTC = re.compile(r"\b([PBCU]\d{4})\b")


def iter_pdf_paths():
    for name in sorted(os.listdir(PDF_DIR)):
        if name.lower().endswith(".pdf"):
            yield os.path.join(PDF_DIR, name)


def extract_lines(path):
    reader = PdfReader(path)
    for page in reader.pages:
        for line in (page.extract_text() or "").splitlines():
            yield line


def extract_refs(section_id, text, part_vocabulary):
    refs = []
    for part in part_vocabulary:
        if part in text:
            refs.append({"section_id": section_id, "ref_type": "PART", "ref_value": part})
    for code in dict.fromkeys(DTC.findall(text)):  # de-dupe, keep order
        refs.append({"section_id": section_id, "ref_type": "CODE", "ref_value": code})
    return refs


def parse_pdf(path, part_vocabulary):
    meta = {}
    sections = []
    current = None  # the section whose body we are reading
    parent_of_depth1 = None

    def close(section):
        if section is not None:
            section["text"] = " ".join(section.pop("_body")).strip()
            sections.append(section)

    for line in extract_lines(path):
        m = META.match(line.strip())
        if m and m.group(1).lower() not in (k.lower() for k in meta):
            meta[m.group(1)] = m.group(2).strip()
            continue
        m = HEADING.match(line)
        if m:
            close(current)
            number, title, ref = m.group(1), m.group(2).strip(), m.group(3)
            depth = number.count(".")
            if depth == 0:
                parent_of_depth1 = ref
                parent = ""
            else:
                parent = parent_of_depth1
            seq = int(number.split(".")[-1])
            current = {
                "id": ref,
                "doc_id": meta.get("Document"),
                "parent_id": parent,
                "seq": seq,
                "title": title,
                "_body": [],
            }
            continue
        if current is not None and line.strip():
            current["_body"].append(line.strip())
    close(current)

    document = {
        "id": meta["Document"],
        "doc_type": meta["Type"],
        "title": next(extract_lines(path), ""),  # placeholder, replaced below
        "model": meta["Model"],
        "published": meta["Published"],
    }
    # The title is the bold line before the metadata block - second non-empty line.
    lines = [ln.strip() for ln in extract_lines(path) if ln.strip()]
    document["title"] = lines[1] if len(lines) > 1 else meta["Document"]

    refs = []
    for s in sections:
        refs.extend(extract_refs(s["id"], s["text"], part_vocabulary))
    return document, sections, refs


def parse_all(part_vocabulary):
    documents, sections, refs = [], [], []
    for path in iter_pdf_paths():
        d, s, r = parse_pdf(path, part_vocabulary)
        documents.append(d)
        sections.extend(s)
        refs.extend(r)
    return documents, sections, refs
