"""Parse the AutoFix PDF library into the ki-style containment model.

Walks sources/pdfs/<folder>/<DOC-ID>.pdf (or a GCS bucket - see
iter_pdf_paths) and produces plain dicts:

- library:   {uri, name, displayName}                       - one root
- folders:   {uri, name, displayName, parent_uri}           - from the path prefixes
- documents: {uri, id, doc_type, title, model, published,
              name, displayName, parent_uri}
- sections:  {uri, name, displayName, headingLevel, content,
              parent_uri, doc_uri, sort_pos}
- refs:      {section_uri, ref_type: PART|CODE, ref_value}
- citations: {section_uri, doc_id}                          - "per recall RC-2021-04"

Model rules (see docs/SHAPE-DESIGN.md):
- URIs are hierarchical slugs: library/folder/file.pdf#heading/path
- Section `content` is Rule 1: the section's own body text followed by
  `uri:` pointer lines for each direct child section
- `sort_pos` is the document-wide DFS reading order (drives NEXT_SECTION)
- Part numbers are recognized against the parts catalog; doc citations
  against the set of document ids; DTCs by the OBD-II pattern

Headings are detected as lines matching `<n>` or `<n>.<m>` numbering, the
convention this library's PDFs print. Real-world parsers key on font data;
numbering is the honest equivalent for text-extraction parsing.

Swap point: iter_pdf_paths() reads sources/pdfs/ by default; set
PDF_SOURCE=gcs with GCS_BUCKET (and optional GCS_PREFIX) to read the same
layout from a cloud bucket.
"""

import os
import re
import tempfile
from pypdf import PdfReader

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_DIR = os.path.join(ROOT, "sources", "pdfs")

LIBRARY_URI = "technical-library"
LIBRARY_NAME = "technical-library"
LIBRARY_DISPLAY = "AutoFix Technical Library"

HEADING = re.compile(r"^(\d+(?:\.\d+)*)\s+(\S.*)$")
META = re.compile(r"^(Document|Type|Model|Published):\s*(.+)$")
DTC = re.compile(r"\b([PBCU]\d{4})\b")


def slugify(text):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s or "untitled"


def iter_pdf_paths():
    """Yield (relative_folder, filename, local_path) for every PDF.

    Local mode walks sources/pdfs/<folder>/. GCS mode (PDF_SOURCE=gcs)
    lists gs://$GCS_BUCKET/$GCS_PREFIX and downloads each object to a
    temp file - same triples, so everything downstream is source-blind.
    """
    if os.environ.get("PDF_SOURCE", "local").lower() == "gcs":
        from google.cloud import storage  # lazy - optional dependency

        bucket_name = os.environ["GCS_BUCKET"]
        prefix = os.environ.get("GCS_PREFIX", "technical-library/").rstrip("/") + "/"
        client = storage.Client.create_anonymous_client() \
            if os.environ.get("GCS_ANONYMOUS", "true").lower() == "true" \
            else storage.Client()
        tmpdir = tempfile.mkdtemp(prefix="autofix-pdfs-")
        for blob in client.list_blobs(bucket_name, prefix=prefix):
            if not blob.name.lower().endswith(".pdf"):
                continue
            rel = blob.name[len(prefix):]
            folder, _, filename = rel.rpartition("/")
            local = os.path.join(tmpdir, filename)
            blob.download_to_filename(local)
            yield folder, filename, local
        return
    for folder in sorted(os.listdir(PDF_DIR)):
        fpath = os.path.join(PDF_DIR, folder)
        if not os.path.isdir(fpath):
            continue
        for name in sorted(os.listdir(fpath)):
            if name.lower().endswith(".pdf"):
                yield folder, name, os.path.join(fpath, name)


def extract_lines(path):
    reader = PdfReader(path)
    for page in reader.pages:
        for line in (page.extract_text() or "").splitlines():
            yield line


def parse_pdf(folder, filename, path):
    """Parse one PDF -> (document dict, [section dicts]) with URIs built."""
    doc_uri = f"{LIBRARY_URI}/{slugify(folder)}/{slugify(filename[:-4])}.pdf"
    meta = {}
    title = None
    sections = []
    stack = []  # [(depth, section_dict)]
    slug_taken = {}  # parent_uri -> {slug: count} for -1/-2 disambiguation
    sort_pos = 0

    def close_body(section):
        section["_body"] = " ".join(section["_body"]).strip()

    for raw in extract_lines(path):
        line = raw.strip()
        if not line:
            continue
        m = META.match(line)
        if m and m.group(1) not in meta:
            meta[m.group(1)] = m.group(2).strip()
            continue
        m = HEADING.match(line)
        if m and meta.get("Published"):  # headings only start after the metadata block
            number, heading = m.group(1), m.group(2).strip()
            depth = number.count(".")
            while stack and stack[-1][0] >= depth:
                close_body(stack.pop()[1])
            parent_uri = stack[-1][1]["uri"] if stack else doc_uri
            base = slugify(heading)
            taken = slug_taken.setdefault(parent_uri, {})
            n = taken.get(base, 0)
            taken[base] = n + 1
            slug = base if n == 0 else f"{base}-{n}"
            frag = f"{stack[-1][1]['_frag']}/{slug}" if stack else slug
            section = {
                "uri": f"{doc_uri}#{frag}",
                "name": frag,
                "displayName": heading,
                "headingLevel": depth + 1,
                "parent_uri": parent_uri,
                "doc_uri": doc_uri,
                "sort_pos": sort_pos,
                "_frag": frag,
                "_body": [],
                "_children": [],
            }
            sort_pos += 1
            if stack:
                stack[-1][1]["_children"].append(section["uri"])
            sections.append(section)
            stack.append((depth, section))
            continue
        if stack:
            stack[-1][1]["_body"].append(line)
        elif title is None and not meta:
            # First non-empty line before any metadata is the library banner;
            # the second is the document title.
            if line != "AutoFix Group Technical Library":
                title = line
        elif title is None:
            title = title  # pragma: no cover

    while stack:
        close_body(stack.pop()[1])

    # Title: the bold line between the banner and the metadata block.
    lines = [ln.strip() for ln in extract_lines(path) if ln.strip()]
    title = lines[1] if len(lines) > 1 else meta.get("Document", filename)

    # Rule 1 content: own body + uri: pointers to direct children.
    for s in sections:
        pointers = "\n".join(f"uri:{c}" for c in s.pop("_children"))
        body = s.pop("_body")
        s["content"] = f"{body}\n{pointers}".strip() if pointers else body
        s.pop("_frag")

    document = {
        "uri": doc_uri,
        "id": meta["Document"],
        "doc_type": meta["Type"],
        "title": title,
        "model": meta["Model"],
        "published": meta["Published"],
        "name": filename,
        "displayName": title,
        "parent_uri": f"{LIBRARY_URI}/{slugify(folder)}",
    }
    return document, sections


def extract_refs(sections, part_vocabulary):
    refs = []
    for s in sections:
        body = s["content"].split("\nuri:")[0]
        for part in part_vocabulary:
            if part in body:
                refs.append({"section_uri": s["uri"], "ref_type": "PART", "ref_value": part})
        for code in dict.fromkeys(DTC.findall(body)):
            refs.append({"section_uri": s["uri"], "ref_type": "CODE", "ref_value": code})
    return refs


def extract_citations(sections, documents):
    """Explicit doc-id mentions in section text -> citation LINKS_TO."""
    by_doc_uri = {d["uri"]: d["id"] for d in documents}
    ids = [d["id"] for d in documents]
    citations = []
    for s in sections:
        body = s["content"].split("\nuri:")[0]
        own = by_doc_uri[s["doc_uri"]]
        for doc_id in ids:
            if doc_id != own and doc_id in body:
                citations.append({"section_uri": s["uri"], "doc_id": doc_id})
    return citations


def parse_all(part_vocabulary):
    library = {"uri": LIBRARY_URI, "name": LIBRARY_NAME, "displayName": LIBRARY_DISPLAY}
    folders_seen = {}
    documents, sections = [], []
    for folder, filename, path in iter_pdf_paths():
        fslug = slugify(folder)
        folders_seen[fslug] = {
            "uri": f"{LIBRARY_URI}/{fslug}",
            "name": fslug,
            "displayName": fslug,
            "parent_uri": LIBRARY_URI,
        }
        d, s = parse_pdf(folder, filename, path)
        documents.append(d)
        sections.extend(s)
    refs = extract_refs(sections, part_vocabulary)
    citations = extract_citations(sections, documents)
    return library, list(folders_seen.values()), documents, sections, refs, citations
