"""Parse the rendered PDF corpus into the domain-agnostic containment model.

Walks sources/pdfs/<area>/<id>.pdf (or a GCS bucket - see iter_pdf_paths) and
produces plain dicts. The model is generic (no domain entities): a containment
tree plus real cross-reference links read from the PDFs' own link annotations.

- library:   {uri, name, displayName}
- folders:   {uri, name, displayName, parent_uri}              (from path prefixes)
- documents: {uri, id, title, area, name, displayName, parent_uri}
- sections:  {uri, name, displayName, headingLevel, content, parent_uri,
              doc_uri, sort_pos}
- links:     {source_uri, target_ref, target_uri|None, external|None, embed}
             source_uri is the Section the link sits in (geometric attribution);
             target_ref is the raw href; target_uri is the resolved in-corpus
             Section/Document uri (None for external URLs -> stub Document).

Headings are detected by `<n>(.<m>)*` numbering, the convention the renderer
prints (PDF text extraction loses font; numbering is the honest signal).
Links are real PDF `/Link` annotations carrying `doc://<id>[#<frag>]` portable
refs or external URLs - no shared-key derivation, no domain coupling.
"""

import os
import re
import tempfile

from pypdf import PdfReader

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_DIR = os.path.join(ROOT, "sources", "pdfs")

LIBRARY_URI = "technical-library"
LIBRARY_DISPLAY = "AutoFix Technical Library"

HEADING = re.compile(r"^(\d+(?:\.\d+)*)\s+(\S.*)$")
META = re.compile(r"^(Document|Area):\s*(.+)$")


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "untitled"


def iter_pdf_paths():
    """Yield (area, filename, local_path). Local walks sources/pdfs/<area>/;
    PDF_SOURCE=gcs lists gs://$GCS_BUCKET/$GCS_PREFIX with the same layout."""
    if os.environ.get("PDF_SOURCE", "local").lower() == "gcs":
        from google.cloud import storage

        bucket = os.environ["GCS_BUCKET"]
        prefix = os.environ.get("GCS_PREFIX", "technical-library/").rstrip("/") + "/"
        client = storage.Client.create_anonymous_client() \
            if os.environ.get("GCS_ANONYMOUS", "true").lower() == "true" else storage.Client()
        tmp = tempfile.mkdtemp(prefix="autofix-corpus-")
        for blob in client.list_blobs(bucket, prefix=prefix):
            if blob.name.lower().endswith(".pdf"):
                rel = blob.name[len(prefix):]
                area, _, filename = rel.rpartition("/")
                local = os.path.join(tmp, filename)
                blob.download_to_filename(local)
                yield area, filename, local
        return
    for area in sorted(os.listdir(PDF_DIR)):
        adir = os.path.join(PDF_DIR, area)
        if os.path.isdir(adir):
            for name in sorted(os.listdir(adir)):
                if name.lower().endswith(".pdf"):
                    yield area, name, os.path.join(adir, name)


def read_positioned(path):
    """-> ([(page, y, line_text)], [(page, y, href)]) in PDF user space.

    Lines are text chunks grouped by (page, rounded-y) and ordered by x; links
    are /Link annotations keyed by their rect mid-y. Heading baselines and link
    rects share the same coordinate space, so reading-order is (page, -y)."""
    reader = PdfReader(path)
    lines, links = [], []
    for pi, page in enumerate(reader.pages):
        chunks = {}  # round(y) -> [(x, text)]

        def visit(text, cm, tm, font_dict, font_size, _ch=chunks):
            if text.strip():
                _ch.setdefault(round(tm[5]), []).append((tm[4], text))

        page.extract_text(visitor_text=visit)
        for y, parts in chunks.items():
            line = "".join(t for _, t in sorted(parts)).strip()
            if line:
                lines.append((pi, y, line))
        for a in (page.get("/Annots") or []):
            o = a.get_object()
            if o.get("/Subtype") == "/Link" and "/A" in o:
                uri = o["/A"].get("/URI")
                if uri:
                    x0, y0, x1, y1 = (float(v) for v in o["/Rect"])
                    links.append((pi, (y0 + y1) / 2, str(uri)))
    lines.sort(key=lambda t: (t[0], -t[1]))
    return lines, links


def parse_pdf(area, filename, path):
    doc_id_slug = slugify(filename[:-4])
    doc_uri = f"{LIBRARY_URI}/{slugify(area)}/{doc_id_slug}.pdf"
    lines, links = read_positioned(path)

    meta, title = {}, None
    sections = []
    stack = []  # [(depth, section)]
    slug_taken = {}
    sort_pos = 0

    for pi, y, line in lines:
        m = META.match(line)
        if m and m.group(1) not in meta:
            meta[m.group(1)] = m.group(2).strip()
            continue
        m = HEADING.match(line)
        if m and meta.get("Area"):  # headings start after the metadata block
            number, heading = m.group(1), m.group(2).strip()
            depth = number.count(".")
            while stack and stack[-1][0] >= depth:
                stack.pop()
            parent_uri = stack[-1][1]["uri"] if stack else doc_uri
            base = slugify(heading)
            taken = slug_taken.setdefault(parent_uri, {})
            n = taken.get(base, 0)
            taken[base] = n + 1
            slug = base if n == 0 else f"{base}-{n}"
            frag = f"{stack[-1][1]['_frag']}/{slug}" if stack else slug
            section = {
                "uri": f"{doc_uri}#{frag}", "name": frag, "displayName": heading,
                "headingLevel": depth + 1, "parent_uri": parent_uri, "doc_uri": doc_uri,
                "sort_pos": sort_pos, "_frag": frag, "_body": [], "_children": [],
                "_page": pi, "_y": y,
            }
            sort_pos += 1
            if stack:
                stack[-1][1]["_children"].append(section["uri"])
            sections.append(section)
            stack.append((depth, section))
            continue
        if title is None and line != "AutoFix Group Technical Library" and not meta:
            title = line
        elif stack:
            stack[-1][1]["_body"].append(line)

    # Rule-1 content: own body + uri: pointers to direct children.
    for s in sections:
        body = " ".join(s["_body"]).strip()
        pointers = "\n".join(f"uri:{c}" for c in s["_children"])
        s["content"] = f"{body}\n{pointers}".strip() if pointers else body

    # Attribute each link to the section it sits in (last section at/above it
    # in reading order), then resolve doc:// refs after all docs are known.
    raw_links = []
    ordered = sorted(sections, key=lambda s: (s["_page"], -s["_y"]))
    for pi, y, href in links:
        key = (pi, -y)
        owner = None
        for s in ordered:
            if (s["_page"], -s["_y"]) <= key:
                owner = s
            else:
                break
        raw_links.append({"source_uri": (owner or sections[0])["uri"], "target_ref": href})

    for s in sections:
        for k in ("_frag", "_body", "_children", "_page", "_y"):
            s.pop(k, None)

    document = {
        "uri": doc_uri, "id": meta.get("Document", doc_id_slug),
        "title": title or filename, "area": slugify(area), "name": filename,
        "displayName": title or filename,
        "parent_uri": f"{LIBRARY_URI}/{slugify(area)}",
    }
    return document, sections, raw_links


def resolve_links(documents, raw_links):
    """doc://<id>[#<frag>] -> in-corpus Section/Document uri; else external stub.
    Dedups (source, target) pairs (multi-line links emit one rect per line)."""
    by_id = {d["id"]: d for d in documents}
    by_id_slug = {slugify(d["id"]): d for d in documents}
    seen, links = set(), []
    for lk in raw_links:
        ref = lk["target_ref"]
        target_uri, external, embed = None, None, False
        if ref.startswith("doc://"):
            rest = ref[len("doc://"):]
            doc_part, _, frag = rest.partition("#")
            doc = by_id.get(doc_part) or by_id_slug.get(slugify(doc_part))
            if doc:
                target_uri = f"{doc['uri']}#{frag}" if frag else doc["uri"]
        else:
            external = ref
        key = (lk["source_uri"], target_uri or external)
        if key in seen:
            continue
        seen.add(key)
        links.append({"source_uri": lk["source_uri"], "target_ref": ref,
                      "target_uri": target_uri, "external": external, "embed": embed})
    return links


def parse_all():
    library = {"uri": LIBRARY_URI, "name": LIBRARY_URI, "displayName": LIBRARY_DISPLAY}
    folders, documents, sections, raw_links = {}, [], [], []
    for area, filename, path in iter_pdf_paths():
        fslug = slugify(area)
        folders[fslug] = {"uri": f"{LIBRARY_URI}/{fslug}", "name": fslug,
                          "displayName": fslug, "parent_uri": LIBRARY_URI}
        d, s, rl = parse_pdf(area, filename, path)
        documents.append(d)
        sections.extend(s)
        raw_links.extend(rl)
    links = resolve_links(documents, raw_links)
    return library, list(folders.values()), documents, sections, links


if __name__ == "__main__":
    lib, folders, docs, sections, links = parse_all()
    print(f"{len(docs)} documents, {len(sections)} sections, {len(links)} links\n")
    for d in docs:
        print(f"  {d['id']:14} {d['uri']}")
    print()
    by_uri = {s["uri"]: s for s in sections}
    for lk in links:
        src = by_uri.get(lk["source_uri"])
        src_name = src["displayName"] if src else lk["source_uri"]
        tgt = lk["target_uri"] or f"[external] {lk['external']}"
        print(f"  LINK  ({src_name}) -> {tgt}")
