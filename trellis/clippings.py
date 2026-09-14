"""Clippings: local full-text copies of the resources a reading points at.

A reading is a *pointer* — title, why-read, and a URL. A clipping is the
*page itself*, saved as markdown inside the vault so studying never leaves
Obsidian. The two are matched by URL, which is deliberately the same key
Obsidian's Web Clipper writes into its `source:` property — so a clipping
can be produced either by `trellis clip` or by clicking the Web Clipper
extension, and both are picked up identically.

Clippings live in `vault/<folder>/clippings/` (the Web Clipper's default
folder name). Cards whose reading has a clipping get an `obsidian://` link
that opens the local copy instead of the browser.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

import yaml

CLIPPINGS_DIRNAME = "clippings"
# A clipping is named after its reading plus this suffix. Obsidian resolves
# a link given as a bare name, which is what makes card links work on a
# phone and a laptop that disagree about where the vault root is — but only
# if the name is unique, so the clipping must not collide with its reading.
CLIP_SUFFIX = "-clip"
# A book's homepage or a docs index extracts cleanly and says nothing. The
# point of a clipping is to lower the cost of getting the information, so a
# page has to carry real prose to earn one.
MIN_PROSE = 2500


@dataclass
class Clipping:
    path: Path
    source_url: str
    title: str
    prose: int = 0
    is_pdf: bool = False

    @property
    def link_target(self) -> str:
        return self.path.stem

    @property
    def is_substantive(self) -> bool:
        """A PDF holds its content in the attachment; anything else has to
        carry the prose itself."""
        return self.is_pdf or self.prose >= MIN_PROSE


def canonical_url(url: str) -> str:
    """Key used to match a clipping to its reading. Ignores the parts that
    don't change which page you land on."""
    parts = urlsplit(url.strip())
    host = parts.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    path = parts.path.rstrip("/")
    return urlunsplit(("https", host, path, parts.query, ""))


class ClipError(RuntimeError):
    """Raised when a page can't be turned into a clipping."""


# Sites serve the modern compressions only to clients that ask for them, and
# hand plain HTML to anything that looks like a script — so the download is
# ours to control, and trafilatura is left to do only what it is best at.
_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def _download(url: str, timeout: int = 30) -> tuple[bytes, str, str]:
    """Returns (body, content-type, charset). Raises ClipError on failure."""
    import gzip
    import socket
    import urllib.request
    import zlib

    # urlopen's timeout does not always cover a connect that never answers,
    # and one dead host must not stall a whole clip run.
    socket.setdefaulttimeout(timeout)

    req = urllib.request.Request(
        url, headers={"User-Agent": _UA, "Accept-Encoding": "gzip, deflate"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            ctype = (resp.headers.get("Content-Type") or "").split(";")[0].strip()
            raw = resp.read()
            encoding = (resp.headers.get("Content-Encoding") or "").lower()
            charset = resp.headers.get_content_charset() or "utf-8"
    except Exception as exc:  # noqa: BLE001 - network failures are expected
        raise ClipError(str(exc)) from exc

    if encoding == "gzip":
        raw = gzip.decompress(raw)
    elif encoding == "deflate":
        raw = zlib.decompress(raw, -zlib.MAX_WBITS)
    return raw, ctype, charset


@dataclass
class FetchedPage:
    """What a URL yielded: either extracted markdown, or a PDF to keep as
    it is — Obsidian renders an embedded PDF, and no conversion beats the
    original for a paper full of diagrams."""

    title: str
    meta: dict = field(default_factory=dict)
    markdown: str = ""
    pdf: bytes | None = None

    @property
    def is_pdf(self) -> bool:
        return self.pdf is not None


def fetch_page(url: str) -> FetchedPage:
    """Download a URL and reduce it to something worth keeping offline.

    Extraction is trafilatura's — the best-scoring open extractor in the
    published benchmarks, and the one that already speaks markdown — so
    this function is only policy: what we refuse to clip, what a PDF does
    instead, and what counts as too little text to be worth keeping.

    Needs the optional `clip` extra: pip install -e '.[clip]'
    """
    try:
        from trafilatura import extract, extract_metadata
    except ImportError as exc:  # pragma: no cover - depends on install
        raise ClipError(
            "clipping needs the optional dependencies: pip install -e '.[clip]'"
        ) from exc

    host = urlsplit(url).netloc.lower().removeprefix("www.")
    if any(host == h or host.endswith("." + h) for h in UNCLIPPABLE_HOSTS):
        raise ClipError(f"{host} pages are the resource itself, not an article")

    raw, ctype, charset = _download(url)
    if ctype == "application/pdf" or url.lower().endswith(".pdf"):
        title = Path(urlsplit(url).path).stem.replace("-", " ").replace("_", " ")
        return FetchedPage(title=title.strip() or host, pdf=raw)
    if "html" not in ctype.lower():
        raise ClipError(f"not an article ({ctype or 'unknown type'})")
    downloaded = raw.decode(charset, errors="replace")

    body = extract(
        downloaded, output_format="markdown",
        include_links=True, include_tables=True,
    )
    if not body:
        # Precision-first extraction returns nothing on pages whose content
        # sits outside a recognisable article element; recall mode keeps
        # some navigation but rescues the text.
        body = extract(
            downloaded, output_format="markdown",
            include_links=True, include_tables=True, favor_recall=True,
        )
    body = re.sub(r"\n{3,}", "\n\n", body or "").strip()
    prose = _prose_length(body)
    if prose < MIN_PROSE:
        raise ClipError(
            f"only {prose} characters of prose — a landing page, index, or "
            "paywall, not an article worth archiving"
        )

    meta = extract_metadata(downloaded, default_url=url)
    extra = {}
    if meta is not None:
        if meta.author:
            extra["author"] = meta.author
        if meta.date:
            extra["published"] = meta.date
        if meta.sitename:
            extra["site"] = meta.sitename
    title = (meta.title if meta is not None and meta.title else "").strip()
    return FetchedPage(title=title, meta=extra, markdown=body)


# Pages that are the resource itself rather than an article: clipping them
# yields navigation chrome, never content.
UNCLIPPABLE_HOSTS = (
    "youtube.com", "youtu.be", "vimeo.com", "twitter.com", "x.com",
)


def _prose_length(markdown_body: str) -> int:
    """Characters left once link markup and headings are removed — a page
    of pure navigation scores near zero even when it looks long."""
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", "", markdown_body)
    text = re.sub(r"^#+ .*$", "", text, flags=re.MULTILINE)
    return len(re.sub(r"\s+", " ", text).strip())


def write_clipping(
    clippings_dir: str | Path, slug: str, url: str, page: FetchedPage, today: str
) -> Path:
    """Write a clipping in the same shape Obsidian's Web Clipper produces,
    so clips made by the extension and by `trellis clip` are
    indistinguishable downstream. A PDF is saved beside its note and
    embedded, which Obsidian renders inline."""
    directory = Path(clippings_dir)
    directory.mkdir(parents=True, exist_ok=True)
    name = f"{slug}{CLIP_SUFFIX}"
    path = directory / f"{name}.md"

    if page.is_pdf:
        (directory / f"{name}.pdf").write_bytes(page.pdf)
        body = f"![[{name}.pdf]]"
    else:
        body = page.markdown

    front = yaml.safe_dump(
        {"title": page.title, "source": url, **page.meta, "clipped": today},
        allow_unicode=True, sort_keys=False,
    )
    path.write_text(f"---\n{front}---\n\n# {page.title}\n\n{body}\n", encoding="utf-8")
    return path


def load_clippings(clippings_dir: str | Path) -> dict[str, Clipping]:
    """Index every clipping under clippings_dir by canonical source URL.
    Files without a `source:` property are ignored (they're notes, not
    clippings)."""
    out: dict[str, Clipping] = {}
    for path in sorted(Path(clippings_dir).rglob("*.md")):
        raw = path.read_text(encoding="utf-8")
        if not raw.startswith("---\n"):
            continue
        try:
            _, front, body = raw.split("---\n", 2)
            meta = yaml.safe_load(front) or {}
        except (ValueError, yaml.YAMLError):
            continue
        if not isinstance(meta, dict):
            continue
        source = meta.get("source")
        if not isinstance(source, str) or not source.startswith("http"):
            continue
        title = str(meta.get("title") or "").strip()
        if not title:
            match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
            title = match.group(1).strip() if match else path.stem
        out[canonical_url(source)] = Clipping(
            path=path, source_url=source, title=title,
            prose=_prose_length(body), is_pdf=".pdf]]" in body,
        )
    return out
