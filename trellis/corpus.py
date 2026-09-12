"""Corpora: bodies of material registered for digestion.

A corpus is a book (an epub, a pdf, or freely published chapters), a blog
series, a course — one thing with an outline of its own. It is declared by
`corpora/<id>.yaml`, the way a codebase is declared by `codebases/<name>.yaml`:

    # corpora/kafka-2e.yaml
    title: Kafka权威指南（第2版）
    author: Gwen Shapira, Todd Palino, Rajini Sivaram, Krit Petty
    license: commercial          # decides where the text may live
    domain: kafka                # the skeleton it lands on (seeded if absent)
    lang: zh                     # language of the text, and of cards written from it
    home: https://www.ituring.com.cn/book/2937
    file: ~/Books/kafka-2e.epub  # a local file, or:
    # chapters: [https://..., https://...]   # freely published chapters

Where the text ends up is decided by the license. Only material its author
or publisher gives away is archived under `sources/archive/<id>/` and
committed. A commercial book you own is ingested into `sources/local/<id>/`,
which git ignores: the text is needed here to triage and digest it, and
nowhere else. Its outline — titles only — is committed for both, so the
Corpus note and the digest plan work on any machine.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

FREE_LICENSES = {"free-online", "cc-by", "cc-by-nc", "cc-by-sa", "public-domain"}
LICENSES = FREE_LICENSES | {"commercial"}
CORPORA_DIRNAME = "corpora"
ARCHIVE_DIRNAME = "sources/archive"     # committed
LOCAL_DIRNAME = "sources/local"         # gitignored
OUTLINES_DIRNAME = "sources/outlines"   # committed: titles, never text
_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class CorpusError(ValueError):
    """Raised for a malformed corpus declaration."""


@dataclass
class Corpus:
    id: str
    title: str
    license: str
    domain: str
    lang: str = "en"
    author: str = ""
    home: str = ""
    file: Path | None = None
    chapters: list[str] = field(default_factory=list)

    @property
    def is_free(self) -> bool:
        return self.license in FREE_LICENSES

    def text_dir(self, root: Path) -> Path:
        """Where the sections' text lives: committed for free material,
        ignored by git for a book you paid for."""
        base = ARCHIVE_DIRNAME if self.is_free else LOCAL_DIRNAME
        return Path(root) / base / self.id

    def outline_path(self, root: Path) -> Path:
        return Path(root) / OUTLINES_DIRNAME / f"{self.id}.yaml"

    @property
    def format(self) -> str:
        """Which ingest adapter reads it: web, epub, pdf, or markdown."""
        if self.chapters:
            return "web"
        suffix = self.file.suffix.lower() if self.file else ""
        return {".epub": "epub", ".pdf": "pdf", ".md": "markdown"}.get(suffix, suffix.lstrip("."))


def load_corpus(path: str | Path) -> Corpus:
    path = Path(path)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise CorpusError(f"{path}: top level must be a mapping")
    errors: list[str] = []
    if not _ID_RE.match(path.stem):
        errors.append(f"id {path.stem!r} must be a lowercase slug (the filename)")
    if not str(data.get("title", "")).strip():
        errors.append("missing title")
    license_ = str(data.get("license", "") or "")
    if license_ not in LICENSES:
        errors.append(f"license must be one of {sorted(LICENSES)}, got {license_!r}")
    domain = str(data.get("domain", "") or "")
    if not re.match(r"^[a-z0-9-]+$", domain):
        errors.append("domain must name a skeleton slug (existing, or to be seeded)")
    file_ = data.get("file")
    chapters = data.get("chapters") or []
    if bool(file_) == bool(chapters):
        errors.append("declare exactly one of 'file' (a local epub/pdf/md) or 'chapters' (URLs)")
    if chapters and not (isinstance(chapters, list) and all(isinstance(c, str) for c in chapters)):
        errors.append("chapters must be a list of URLs")
    if chapters and license_ not in FREE_LICENSES:
        errors.append("chapters can only be fetched for a freely licensed corpus")
    unknown = set(data) - {"title", "author", "license", "domain", "lang", "home", "file", "chapters"}
    if unknown:
        errors.append(f"unknown keys {sorted(unknown)}")
    if errors:
        raise CorpusError(f"{path}:\n  " + "\n  ".join(errors))
    return Corpus(
        id=path.stem,
        title=str(data["title"]).strip(),
        license=license_,
        domain=domain,
        lang=str(data.get("lang", "en") or "en"),
        author=str(data.get("author", "") or ""),
        home=str(data.get("home", "") or ""),
        file=Path(str(file_)).expanduser() if file_ else None,
        chapters=list(chapters),
    )


def load_corpora(root: Path) -> dict[str, Corpus]:
    """Every declared corpus, by id. A malformed declaration raises."""
    directory = Path(root) / CORPORA_DIRNAME
    if not directory.exists():
        return {}
    return {p.stem: load_corpus(p) for p in sorted(directory.glob("*.yaml"))}


@dataclass
class Section:
    """One unit of a corpus as its outline defines it: a chapter, or a
    heading below one. `id` is the archived file's stem and the handle
    every reading written from it carries."""

    id: str
    title: str
    level: int
    ordinal: int
    children: list[str] = field(default_factory=list)  # sub-heading titles
    locator: str = ""     # URL, or "p. 12-19", or the epub file: where to find it
    text: str = ""        # markdown; empty once loaded from the outline alone


@dataclass
class Outline:
    corpus: str
    title: str
    sections: list[Section]

    def by_id(self) -> dict[str, Section]:
        return {s.id: s for s in self.sections}

    def dump(self) -> str:
        data = {
            "corpus": self.corpus,
            "title": self.title,
            "sections": [
                {k: v for k, v in {
                    "id": s.id, "title": s.title, "level": s.level,
                    "children": s.children or None, "locator": s.locator or None,
                }.items() if v is not None}
                for s in self.sections
            ],
        }
        return yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=100)


def load_outline(path: str | Path) -> Outline:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    sections = [
        Section(id=str(s["id"]), title=str(s["title"]), level=int(s.get("level", 1)),
                ordinal=i, children=list(s.get("children") or []),
                locator=str(s.get("locator") or ""))
        for i, s in enumerate(data.get("sections") or [])
    ]
    return Outline(corpus=str(data["corpus"]), title=str(data.get("title", "")),
                   sections=sections)


def slugify(title: str, fallback: str = "section") -> str:
    """ASCII slug from a title that may be mostly CJK: keeps digits and
    latin words, so `3.4 生产者配置` becomes `3-4` and
    `第4章 Kafka消费者` becomes `4-kafka`."""
    ascii_ = re.sub(r"[^A-Za-z0-9]+", "-", title).strip("-").lower()
    return ascii_ or fallback
