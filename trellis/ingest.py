"""Ingest: a corpus becomes archived sections and an outline.

One interface — `extract(corpus) -> Outline` with each section's text — and
one adapter per format behind it:

    web       freely published chapters, fetched page by page and
              checkpointed in pipeline/state/ingest-<id>.json so a run
              killed mid-book resumes where it stopped
    epub      the OPF spine for order, the NCX / EPUB3 nav for the outline,
              our own HTML→markdown for the text (no dependencies)
    pdf       the document's bookmarks for the outline, page ranges for the
              text (needs the optional `ingest` extra: PyMuPDF); a pdf
              without bookmarks degrades to fixed page runs, and says so
    markdown  one file split at its headings — the escape hatch for
              anything converted by hand

`ingest()` writes the sections into the corpus's text directory (committed
for free material, gitignored for a book you paid for) and the outline —
titles only — into sources/outlines/, which is committed either way.
"""

from __future__ import annotations

import datetime as dt
import json
import posixpath
import re
import zipfile
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote
from xml.etree import ElementTree as ET

import yaml

from .corpus import Corpus, Outline, Section, slugify

STATE_DIRNAME = "pipeline/state"


class IngestError(RuntimeError):
    """Raised when a corpus cannot be read at all."""


# --------------------------------------------------------------------------
# HTML -> markdown, small and predictable. Article extractors are tuned for
# web pages full of chrome; an epub chapter is already just the content, and
# what matters is not losing code blocks, lists and tables.

_BLOCK = {"p", "div", "section", "article", "h1", "h2", "h3", "h4", "h5", "h6",
          "ul", "ol", "li", "pre", "blockquote", "table", "tr", "figure",
          "figcaption", "dl", "dt", "dd", "hr", "body"}
_SKIP = {"script", "style", "head", "title", "nav", "svg"}


class _Markdown(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.skip = 0
        self.pre = 0
        self.lists: list[tuple[str, int]] = []   # (kind, counter)
        self.cell: list[str] | None = None
        self.row: list[str] = []
        self.table_rows = 0
        self.href: str | None = None
        self.quote = 0

    # -- helpers
    def _emit(self, text: str) -> None:
        if self.cell is not None:
            self.cell.append(text)
        else:
            self.out.append(text)

    def _newline(self, n: int = 2) -> None:
        if self.cell is not None:
            return
        joined = "".join(self.out)
        trailing = len(joined) - len(joined.rstrip("\n"))
        if trailing < n:
            self.out.append("\n" * (n - trailing))

    # -- parser callbacks
    def handle_starttag(self, tag: str, attrs: list) -> None:
        a = dict(attrs)
        if tag in _SKIP:
            self.skip += 1
            return
        if self.skip:
            return
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._newline()
            self._emit("#" * int(tag[1]) + " ")
        elif tag == "p":
            self._newline()
            if self.quote:
                self._emit("> ")
        elif tag == "br":
            self._emit("\n")
        elif tag == "hr":
            self._newline()
            self._emit("---")
            self._newline()
        elif tag in ("ul", "ol"):
            self._newline()
            self.lists.append((tag, 0))
        elif tag == "li":
            self._newline(1)
            kind, n = self.lists[-1] if self.lists else ("ul", 0)
            indent = "  " * (len(self.lists) - 1)
            if kind == "ol":
                n += 1
                self.lists[-1] = (kind, n)
                self._emit(f"{indent}{n}. ")
            else:
                self._emit(f"{indent}- ")
        elif tag == "pre":
            self._newline()
            self._emit("```\n")
            self.pre += 1
        elif tag == "code" and not self.pre:
            self._emit("`")
        elif tag in ("strong", "b"):
            self._emit("**")
        elif tag in ("em", "i"):
            self._emit("*")
        elif tag == "blockquote":
            self._newline()
            self.quote += 1
        elif tag == "img":
            alt = (a.get("alt") or "").strip()
            self._emit(f"![{alt}]" if alt else "")
        elif tag == "a":
            self.href = a.get("href")
            if self.href and self.href.startswith("http"):
                self._emit("[")
            else:
                self.href = None
        elif tag == "table":
            self._newline()
            self.table_rows = 0
        elif tag == "tr":
            self.row = []
        elif tag in ("td", "th"):
            self.cell = []
        elif tag in ("div", "section", "article", "figure", "figcaption", "dd", "dt"):
            self._newline()

    def handle_endtag(self, tag: str) -> None:
        if tag in _SKIP:
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6", "p", "div", "section",
                   "article", "figure", "figcaption", "dd", "dt"):
            self._newline()
        elif tag in ("ul", "ol"):
            if self.lists:
                self.lists.pop()
            self._newline()
        elif tag == "li":
            self._newline(1)
        elif tag == "pre":
            self.pre = max(0, self.pre - 1)
            self._newline(1)
            self._emit("```")
            self._newline()
        elif tag == "code" and not self.pre:
            self._emit("`")
        elif tag in ("strong", "b"):
            self._emit("**")
        elif tag in ("em", "i"):
            self._emit("*")
        elif tag == "blockquote":
            self.quote = max(0, self.quote - 1)
            self._newline()
        elif tag == "a" and self.href:
            self._emit(f"]({self.href})")
            self.href = None
        elif tag in ("td", "th"):
            text = re.sub(r"\s+", " ", "".join(self.cell or [])).strip()
            self.row.append(text)
            self.cell = None
        elif tag == "tr":
            if self.row:
                self.out.append("| " + " | ".join(self.row) + " |\n")
                self.table_rows += 1
                if self.table_rows == 1:
                    self.out.append("|" + "---|" * len(self.row) + "\n")
            self.row = []
        elif tag == "table":
            self._newline()

    def handle_data(self, data: str) -> None:
        if self.skip:
            return
        if self.pre:
            self._emit(data)
        else:
            text = re.sub(r"[ \t\r\n]+", " ", data)
            if text.strip() or (self.out and not self.out[-1].endswith("\n")):
                self._emit(text)

    def text(self) -> str:
        body = "".join(self.out)
        body = re.sub(r"[ \t]+\n", "\n", body)
        body = re.sub(r"\n{3,}", "\n\n", body)
        return body.strip()


def html_to_markdown(html: str) -> str:
    parser = _Markdown()
    parser.feed(html)
    parser.close()
    return parser.text()


# --------------------------------------------------------------------------
# epub

_NS = {
    "opf": "http://www.idpf.org/2007/opf",
    "dc": "http://purl.org/dc/elements/1.1/",
    "ncx": "http://www.daisy.org/z3986/2005/ncx/",
    "xhtml": "http://www.w3.org/1999/xhtml",
    "epub": "http://www.idpf.org/2007/ops",
    "c": "urn:oasis:names:tc:opendocument:xmlns:container",
}


@dataclass
class _NavEntry:
    title: str
    file: str       # zip member path, fragment stripped
    depth: int


def _read_epub_nav(z: zipfile.ZipFile, opf_dir: str, manifest: dict, spine_toc: str | None,
                   ) -> list[_NavEntry]:
    """The table of contents as a flat list in reading order, from an NCX
    (EPUB 2) or a nav document (EPUB 3), whichever the book carries."""
    entries: list[_NavEntry] = []

    def member(href: str) -> str:
        return posixpath.normpath(posixpath.join(opf_dir, unquote(href.split("#")[0])))

    nav_href = next((h for h, (mt, props) in manifest.items() if "nav" in props.split()), None)
    if nav_href:
        doc = ET.fromstring(z.read(member(nav_href)))
        nav_dir = posixpath.dirname(member(nav_href))
        tocs = [n for n in doc.iter(f"{{{_NS['xhtml']}}}nav")
                if n.get(f"{{{_NS['epub']}}}type") == "toc"] or list(doc.iter(f"{{{_NS['xhtml']}}}nav"))
        if tocs:
            def walk(ol, depth):
                for li in ol.findall(f"{{{_NS['xhtml']}}}li"):
                    a = li.find(f"{{{_NS['xhtml']}}}a")
                    if a is not None and a.get("href"):
                        title = "".join(a.itertext()).strip()
                        target = posixpath.normpath(posixpath.join(nav_dir, unquote(a.get("href").split("#")[0])))
                        entries.append(_NavEntry(title, target, depth))
                    for sub in li.findall(f"{{{_NS['xhtml']}}}ol"):
                        walk(sub, depth + 1)
            for ol in tocs[0].findall(f"{{{_NS['xhtml']}}}ol"):
                walk(ol, 1)
            if entries:
                return entries

    ncx_href = manifest.get(spine_toc, (None, ""))[0] if spine_toc else None
    if ncx_href is None:
        ncx_href = next((h for h, (mt, _) in manifest.items() if mt == "application/x-dtbncx+xml"), None)
    if ncx_href:
        doc = ET.fromstring(z.read(member(ncx_href)))
        ncx_dir = posixpath.dirname(member(ncx_href))

        def walk_ncx(node, depth):
            for point in node.findall(f"{{{_NS['ncx']}}}navPoint"):
                label = point.find(f"{{{_NS['ncx']}}}navLabel/{{{_NS['ncx']}}}text")
                content = point.find(f"{{{_NS['ncx']}}}content")
                if label is not None and content is not None and content.get("src"):
                    title = (label.text or "").strip()
                    target = posixpath.normpath(posixpath.join(ncx_dir, unquote(content.get("src").split("#")[0])))
                    entries.append(_NavEntry(title, target, depth))
                walk_ncx(point, depth + 1)

        nav_map = doc.find(f"{{{_NS['ncx']}}}navMap")
        if nav_map is not None:
            walk_ncx(nav_map, 1)
    return entries


def extract_epub(path: Path, corpus_id: str) -> tuple[Outline, list[str]]:
    """Sections follow the table of contents: a section is the first nav
    entry that points at a file, its children are the later entries that
    point into the same file, and spine files no entry names are folded
    into the section before them (a chapter split across files)."""
    notes: list[str] = []
    try:
        z = zipfile.ZipFile(path)
    except (OSError, zipfile.BadZipFile) as exc:
        raise IngestError(f"{path}: not an epub ({exc})") from exc
    with z:
        container = ET.fromstring(z.read("META-INF/container.xml"))
        rootfile = container.find(".//c:rootfile", _NS)
        if rootfile is None:
            raise IngestError(f"{path}: container.xml names no rootfile")
        opf_path = rootfile.get("full-path")
        opf_dir = posixpath.dirname(opf_path)
        opf = ET.fromstring(z.read(opf_path))
        title_el = opf.find(".//dc:title", _NS)
        book_title = (title_el.text or "").strip() if title_el is not None else path.stem

        manifest: dict[str, tuple[str, str]] = {}   # href -> (media-type, properties)
        by_id: dict[str, str] = {}
        for item in opf.iter(f"{{{_NS['opf']}}}item"):
            manifest[item.get("href")] = (item.get("media-type", ""), item.get("properties", ""))
            by_id[item.get("id")] = item.get("href")
        spine_el = opf.find("opf:spine", _NS)
        spine_toc = spine_el.get("toc") if spine_el is not None else None
        spine = [posixpath.normpath(posixpath.join(opf_dir, unquote(by_id[ref.get("idref")])))
                 for ref in opf.iter(f"{{{_NS['opf']}}}itemref") if ref.get("idref") in by_id]

        nav = _read_epub_nav(z, opf_dir, manifest, spine_toc)
        if not nav:
            notes.append("no table of contents in the epub — one section per spine file")
            nav = [_NavEntry(f"Part {i + 1}", f, 1) for i, f in enumerate(spine)]

        sections: list[Section] = []
        owner: dict[str, Section] = {}
        for entry in nav:
            if entry.file in owner:
                owner[entry.file].children.append(entry.title)
                continue
            section = Section(id="", title=entry.title, level=entry.depth,
                              ordinal=len(sections), locator=entry.file)
            sections.append(section)
            owner[entry.file] = section

        # Text follows the spine; a file the outline never names continues
        # the section before it.
        current: Section | None = None
        texts: dict[int, list[str]] = {}
        for file in spine:
            if file not in z.namelist():
                continue
            mt = manifest.get(posixpath.relpath(file, opf_dir) if opf_dir else file, ("", ""))[0]
            if mt and "html" not in mt and "xml" not in mt:
                continue
            if file in owner:
                current = owner[file]
            if current is None:
                continue
            texts.setdefault(current.ordinal, []).append(
                html_to_markdown(z.read(file).decode("utf-8", "replace")))

        width = max(3, len(str(len(sections))))
        for section in sections:
            section.id = f"{section.ordinal + 1:0{width}d}-{slugify(section.title)}"
            section.text = "\n\n".join(t for t in texts.get(section.ordinal, []) if t).strip()
            if not section.text:
                notes.append(f"{section.id}: outline names it but no text was found")
    return Outline(corpus=corpus_id, title=book_title, sections=sections), notes


# --------------------------------------------------------------------------
# pdf

def extract_pdf(path: Path, corpus_id: str, run: int = 8) -> tuple[Outline, list[str]]:
    """Bookmarks give the outline: entries down to level 2 become sections,
    deeper ones their children. Without bookmarks the book is cut into runs
    of `run` pages, which is honest but useless for triage — say so."""
    try:
        import pymupdf
    except ImportError:  # pragma: no cover - depends on install
        try:
            import fitz as pymupdf  # the pre-1.24 name
        except ImportError as exc:
            raise IngestError("reading a pdf needs the optional dependency: "
                              "pip install -e '.[ingest]'") from exc
    notes: list[str] = []
    doc = pymupdf.open(str(path))
    toc = [(int(lvl), str(title).strip(), int(page)) for lvl, title, page in doc.get_toc()]
    title = (doc.metadata or {}).get("title") or path.stem

    starts: list[tuple[str, int, int, list[str]]] = []   # title, level, first page, children
    if toc:
        for lvl, t, page in toc:
            if lvl <= 2:
                starts.append((t, lvl, max(1, page), []))
            elif starts:
                starts[-1][3].append(t)
    else:
        notes.append(f"no bookmarks in the pdf — cut into runs of {run} pages")
        for first in range(1, doc.page_count + 1, run):
            last = min(first + run - 1, doc.page_count)
            starts.append((f"Pages {first}-{last}", 1, first, []))

    sections: list[Section] = []
    width = max(3, len(str(len(starts))))
    for i, (t, lvl, first, children) in enumerate(starts):
        last = (starts[i + 1][2] - 1) if i + 1 < len(starts) else doc.page_count
        last = max(first, last)
        text = "\n\n".join(doc[p - 1].get_text("text").strip() for p in range(first, last + 1))
        sections.append(Section(
            id=f"{i + 1:0{width}d}-{slugify(t)}", title=t, level=lvl, ordinal=i,
            children=children, locator=f"p. {first}-{last}", text=text.strip(),
        ))
    return Outline(corpus=corpus_id, title=title, sections=sections), notes


# --------------------------------------------------------------------------
# markdown: one file, split at its headings

_HEADING_RE = re.compile(r"^(#{1,3})\s+(.+?)\s*$", re.MULTILINE)


def extract_markdown(path: Path, corpus_id: str) -> tuple[Outline, list[str]]:
    raw = path.read_text(encoding="utf-8")
    if raw.startswith("---\n"):
        parts = raw.split("---\n", 2)
        raw = parts[2] if len(parts) == 3 else raw
    matches = list(_HEADING_RE.finditer(raw))
    if not matches:
        return Outline(corpus_id, path.stem, [Section(
            id="001-" + slugify(path.stem), title=path.stem, level=1, ordinal=0,
            text=raw.strip())]), ["no headings — the whole file is one section"]
    # The shallowest heading level is the section level; anything deeper
    # stays inside its section as a child heading.
    section_level = min(len(m.group(1)) for m in matches)
    starts: list[tuple[str, int, int, list[str]]] = []   # title, level, offset, children
    for m in matches:
        level = len(m.group(1))
        if level > section_level and starts:
            starts[-1][3].append(m.group(2))
        else:
            starts.append((m.group(2), level, m.start(), []))
    width = max(3, len(str(len(starts))))
    sections = []
    for i, (title, level, offset, children) in enumerate(starts):
        end = starts[i + 1][2] if i + 1 < len(starts) else len(raw)
        sections.append(Section(
            id=f"{i + 1:0{width}d}-{slugify(title)}", title=title, level=level,
            ordinal=i, children=children, text=raw[offset:end].strip(),
        ))
    return Outline(corpus_id, path.stem, sections), []


# --------------------------------------------------------------------------
# web: freely published chapters, fetched with the clippings machinery

def _state_path(root: Path, corpus_id: str) -> Path:
    return Path(root) / STATE_DIRNAME / f"ingest-{corpus_id}.json"


def _load_state(root: Path, corpus_id: str) -> dict:
    path = _state_path(root, corpus_id)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"corpus": corpus_id, "chapters": {}}


def _save_state(root: Path, corpus_id: str, state: dict) -> None:
    state["corpus"] = corpus_id
    state.pop("book", None)
    state["updated"] = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    path = _state_path(root, corpus_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
                    encoding="utf-8")


def _url_slug(url: str) -> str:
    tail = url.rstrip("/").rsplit("/", 1)[-1]
    return slugify(re.sub(r"\.[a-z]+$", "", tail), "chapter")


def extract_web(corpus: Corpus, root: Path, retry: bool = False,
                fetch=None) -> tuple[Outline, list[str]]:
    """Each chapter URL is one section. Fetches are checkpointed per
    chapter, so a run killed by the network resumes; `retry` re-attempts
    chapters marked failed. `fetch` is injectable for tests."""
    from .clippings import ClipError, fetch_page
    fetch = fetch or fetch_page
    state = _load_state(root, corpus.id)
    text_dir = corpus.text_dir(root)
    notes: list[str] = []
    sections: list[Section] = []
    width = max(2, len(str(len(corpus.chapters))))
    for i, url in enumerate(corpus.chapters, start=1):
        entry = state["chapters"].get(url, {})
        section_id = f"{i:0{width}d}-{_url_slug(url)}"
        existing = text_dir / f"{section_id}.md"
        if entry.get("file") and Path(root, entry["file"]).exists() and entry.get("status") == "done":
            existing = Path(root, entry["file"])
            section_id = existing.stem
        if entry.get("status") == "done" and existing.exists():
            title, text = _read_section_file(existing)
            sections.append(Section(id=section_id, title=title, level=1,
                                    ordinal=len(sections), locator=url, text=text))
            continue
        if entry.get("status") == "failed" and not retry:
            notes.append(f"{section_id}: failed last time, pass --retry to try again")
            continue
        try:
            page = fetch(url)
        except ClipError as exc:
            state["chapters"][url] = {"status": "failed", "error": str(exc)}
            _save_state(root, corpus.id, state)
            notes.append(f"{section_id}: FAILED {exc}")
            continue
        if page.is_pdf:
            dest = text_dir / f"{section_id}.pdf"
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(page.pdf)
            notes.append(f"{section_id}: a pdf, saved as is")
            state["chapters"][url] = {"status": "done", "file": str(dest.relative_to(root))}
            _save_state(root, corpus.id, state)
            continue
        section = Section(id=section_id, title=page.title or section_id, level=1,
                          ordinal=len(sections), locator=url, text=page.markdown.strip())
        write_section(corpus, root, section)
        state["chapters"][url] = {"status": "done",
                                  "file": str((text_dir / f"{section_id}.md").relative_to(root))}
        _save_state(root, corpus.id, state)
        sections.append(section)
    return Outline(corpus=corpus.id, title=corpus.title, sections=sections), notes


def _read_section_file(path: Path) -> tuple[str, str]:
    raw = path.read_text(encoding="utf-8")
    title = path.stem
    if raw.startswith("---\n"):
        parts = raw.split("---\n", 2)
        if len(parts) == 3:
            meta = yaml.safe_load(parts[1]) or {}
            title = str(meta.get("title") or title)
            raw = parts[2]
    return title, raw.strip()


# --------------------------------------------------------------------------

@dataclass
class IngestResult:
    outline: Outline
    written: list[Path] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def write_section(corpus: Corpus, root: Path, section: Section) -> Path:
    directory = corpus.text_dir(root)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{section.id}.md"
    front = yaml.safe_dump(
        {"title": section.title, "corpus": corpus.id, "section": section.id,
         "level": section.level, "locator": section.locator or None,
         "license": corpus.license,
         "fetched": dt.date.today().isoformat()},
        allow_unicode=True, sort_keys=False,
    )
    path.write_text(f"---\n{front}---\n\n{section.text.strip()}\n", encoding="utf-8")
    return path


def extract(corpus: Corpus, root: Path, retry: bool = False, fetch=None,
            ) -> tuple[Outline, list[str]]:
    fmt = corpus.format
    if fmt == "web":
        return extract_web(corpus, root, retry=retry, fetch=fetch)
    if corpus.file is None or not corpus.file.exists():
        raise IngestError(f"{corpus.id}: file not found: {corpus.file}")
    if fmt == "epub":
        return extract_epub(corpus.file, corpus.id)
    if fmt == "pdf":
        return extract_pdf(corpus.file, corpus.id)
    if fmt == "markdown":
        return extract_markdown(corpus.file, corpus.id)
    raise IngestError(f"{corpus.id}: no adapter for '{fmt}' files")


def ingest(corpus: Corpus, root: Path, retry: bool = False, fetch=None) -> IngestResult:
    """Extract, write the sections' text where the license allows it to
    live, and the outline where it can always live."""
    outline, notes = extract(corpus, root, retry=retry, fetch=fetch)
    result = IngestResult(outline=outline, notes=notes)
    if corpus.format != "web":   # web sections are written as they land
        for section in outline.sections:
            result.written.append(write_section(corpus, root, section))
    outline_path = corpus.outline_path(root)
    outline_path.parent.mkdir(parents=True, exist_ok=True)
    outline_path.write_text(outline.dump(), encoding="utf-8")
    result.written.append(outline_path)
    return result
