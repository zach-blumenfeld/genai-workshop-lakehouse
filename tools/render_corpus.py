"""Render the authored markdown corpus to PDFs with embedded cross-reference links.

Markdown is the source of truth. Each `corpus/<area>/<id>.md` has YAML-ish
frontmatter (id, title, area) and a controlled markdown subset:

- ATX headings `#`, `##`, `###` ...  -> auto-numbered (1, 1.1, ...) so the
  text-extraction loader can detect them (PDF text loses font, numbering is the
  honest heading signal).
- paragraphs of prose.
- inline links `[text](href)` where href is a portable `doc://<id>[#<frag>]`
  cross-reference or an external `https://...` URL. Each link is emitted as a
  real PDF link annotation (extracted later by load/).

Output mirrors the source layout: sources/pdfs/<area>/<id>.pdf — so a GCS
bucket with the same prefixes yields the same :Folder nodes.

Run: .venv/bin/python tools/render_corpus.py
"""

import os
import re
import shutil

from reportlab.lib.pagesizes import LETTER
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS_DIR = os.path.join(ROOT, "corpus")
PDF_DIR = os.path.join(ROOT, "sources", "pdfs")

PAGE_W, PAGE_H = LETTER
MARGIN = 60
LINE_H = 15
BODY_FONT, BODY_SIZE = "Helvetica", 10
HEAD_FONT = "Helvetica-Bold"
HEAD_SIZE = {1: 14, 2: 12, 3: 11}
SPACE_W = stringWidth(" ", BODY_FONT, BODY_SIZE)

LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
BANNER = "AutoFix Group Technical Library"


def parse_md(path):
    """-> (meta dict, [blocks]). Block: ('h', level, text) or ('p', [(word, href)])."""
    text = open(path).read()
    meta = {}
    body = text
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        for line in fm.strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()

    blocks = []
    for para in re.split(r"\n\s*\n", body.strip()):
        para = para.strip()
        if not para:
            continue
        m = re.match(r"^(#+)\s+(.*)$", para)
        if m:
            blocks.append(("h", len(m.group(1)), m.group(2).strip()))
            continue
        # paragraph: flatten to words, each carrying its link href (or None)
        flat = " ".join(para.split())
        words, pos = [], 0
        for lm in LINK.finditer(flat):
            for w in flat[pos:lm.start()].split():
                words.append((w, None))
            for w in lm.group(1).split():
                words.append((w, lm.group(2)))
            pos = lm.end()
        for w in flat[pos:].split():
            words.append((w, None))
        blocks.append(("p", words))
    return meta, blocks


class Renderer:
    def __init__(self, path):
        self.c = canvas.Canvas(path, pagesize=LETTER)
        self.y = PAGE_H - MARGIN

    def _newline(self, h=LINE_H):
        self.y -= h
        if self.y < MARGIN:
            self.c.showPage()
            self.y = PAGE_H - MARGIN

    def text_line(self, s, font=BODY_FONT, size=BODY_SIZE):
        self.c.setFont(font, size)
        self.c.drawString(MARGIN, self.y, s)
        self._newline()

    def heading(self, number, title, level):
        self._newline(LINE_H // 2)
        self.text_line(f"{number} {title}", HEAD_FONT, HEAD_SIZE.get(level, 11))

    def paragraph(self, words):
        """Flow words with wrapping; emit a link annotation per (href, line) span."""
        self.c.setFont(BODY_FONT, BODY_SIZE)
        x = MARGIN
        max_x = PAGE_W - MARGIN
        pending = {}  # href -> [x0, x1] for the current line

        def flush_line():
            for href, (x0, x1) in pending.items():
                self.c.linkURL(href, (x0, self.y - 3, x1, self.y + BODY_SIZE), relative=0)
            pending.clear()

        for word, href in words:
            w = stringWidth(word, BODY_FONT, BODY_SIZE)
            if x + w > max_x:  # wrap
                flush_line()
                self.y -= LINE_H
                if self.y < MARGIN:
                    self.c.showPage()
                    self.y = PAGE_H - MARGIN
                    self.c.setFont(BODY_FONT, BODY_SIZE)
                x = MARGIN
            self.c.drawString(x, self.y, word)
            if href:
                span = pending.setdefault(href, [x, x])
                span[1] = x + w
            x += w + SPACE_W
        flush_line()
        self._newline()

    def save(self):
        self.c.save()


def render(path, out_path):
    meta, blocks = parse_md(path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    r = Renderer(out_path)
    r.text_line(BANNER, "Helvetica-Oblique", 9)
    r.text_line(meta["title"], HEAD_FONT, 15)
    r.text_line(f"Document: {meta['id']}")
    r.text_line(f"Area: {meta['area']}")
    r._newline(LINE_H // 2)

    counters = [0, 0, 0, 0, 0, 0]
    for block in blocks:
        if block[0] == "h":
            level = block[1]
            counters[level - 1] += 1
            for i in range(level, len(counters)):
                counters[i] = 0
            number = ".".join(str(counters[i]) for i in range(level))
            r.heading(number, block[2], level)
        else:
            r.paragraph(block[1])
    r.save()


def main():
    if os.path.isdir(PDF_DIR):
        shutil.rmtree(PDF_DIR)
    count = 0
    for area in sorted(os.listdir(CORPUS_DIR)):
        adir = os.path.join(CORPUS_DIR, area)
        if not os.path.isdir(adir):
            continue
        for name in sorted(os.listdir(adir)):
            if name.endswith(".md"):
                doc_id = name[:-3]
                out = os.path.join(PDF_DIR, area, f"{doc_id}.pdf")
                render(os.path.join(adir, name), out)
                print(f"pdfs/{area}/{doc_id}.pdf")
                count += 1
    print(f"rendered {count} document(s)")


if __name__ == "__main__":
    main()
