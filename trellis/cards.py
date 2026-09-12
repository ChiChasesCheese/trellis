"""Cards: Obsidian-native markdown files that compile to Anki notes.

A card lives anywhere under vault/cards/ and looks like:

    ---
    id: cap-theorem
    node: consistency.cap
    type: qa            # qa (default) | cloze
    tags: [tradeoffs]   # optional extra Anki tags
    source: primer      # optional attribution key
    ---
    ## Q
    What does the CAP theorem state?
    ## A
    During a network partition, a distributed system must choose ...

Cloze cards have no Q/A sections; the body holds Anki cloze syntax:

    ---
    id: quorum-formula
    node: storage.replication
    type: cloze
    ---
    A quorum needs {{c1::W + R > N}} to guarantee read-your-writes.

The card `id` is the Anki GUID: rename it and Anki treats the card as new;
keep it and edits update the existing card in place.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_CLOZE_RE = re.compile(r"\{\{c\d+::")
CARD_TYPES = ("qa", "cloze")


class CardError(ValueError):
    """Raised for a card file that violates the format."""


@dataclass
class Card:
    id: str
    node: str
    type: str
    path: Path
    question: str = ""
    answer: str = ""
    text: str = ""  # cloze body
    tags: list[str] = field(default_factory=list)
    source: str = ""
    tr: dict = field(default_factory=dict)  # lang -> {question, answer} | {text}

    def render(self, lang: str = "") -> tuple[str, str]:
        """(question, answer) for a qa card, (text, "") for a cloze —
        in `lang` where it exists, in English where it does not, so an
        untranslated card still builds."""
        parts = self.tr.get(lang, {}) if lang else {}
        if self.type == "cloze":
            return parts.get("text") or self.text, ""
        return (parts.get("question") or self.question,
                parts.get("answer") or self.answer)


def _split_frontmatter(raw: str, path: Path) -> tuple[dict, str]:
    if not raw.startswith("---\n"):
        raise CardError(f"{path}: missing YAML frontmatter")
    try:
        _, fm, body = raw.split("---\n", 2)
    except ValueError:
        raise CardError(f"{path}: unterminated frontmatter") from None
    meta = yaml.safe_load(fm)
    if not isinstance(meta, dict):
        raise CardError(f"{path}: frontmatter must be a mapping")
    return meta, body.strip()


_SECTION_RE = re.compile(r"^##[ \t]+(.+?)[ \t]*$", re.MULTILINE)
_LANG_RE = re.compile(r"^(?:(q|a)[ \t]+)?([a-z]{2}(?:-[a-z]{2})?)$")


def _sections(body: str) -> tuple[str, dict[str, str]]:
    """Split a card body into its `##` sections, keeping whatever precedes
    the first heading (a cloze card is written without headings)."""
    marks = list(_SECTION_RE.finditer(body))
    preamble = (body[: marks[0].start()] if marks else body).strip()
    out: dict[str, str] = {}
    for i, mark in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(body)
        name = mark.group(1).strip().lower()
        if name in out:
            # Two writers appending a translation to the same card would
            # otherwise leave one silently shadowing the other.
            raise CardError(f"repeated section '## {mark.group(1).strip()}'")
        out[name] = body[mark.end():end].strip()
    return preamble, out


def _translations(sections: dict[str, str], path: Path, cloze: bool,
                  sections_text: str = "") -> dict:
    """Language variants written beside the English body: `## Q zh` and
    `## A zh` for a qa card, `## zh` for a cloze. English is never
    replaced, so a translation can always be redone or dropped."""
    langs: dict[str, dict[str, str]] = {}
    for name, content in sections.items():
        if name in ("q", "a"):
            continue
        match = _LANG_RE.match(name)
        if not match:
            raise CardError(
                f"{path}: unknown section '## {name}' — expected 'Q'/'A', "
                "a translated 'Q <lang>'/'A <lang>', or '<lang>' for a cloze"
            )
        part, lang = match.group(1), match.group(2)
        if cloze and part is None:
            langs.setdefault(lang, {})["text"] = content
        elif not cloze and part is not None:
            langs.setdefault(lang, {})["question" if part == "q" else "answer"] = content
        else:
            raise CardError(f"{path}: '## {name}' does not fit a {'cloze' if cloze else 'qa'} card")
    for lang, parts in langs.items():
        missing = ({"question", "answer"} if not cloze else {"text"}) - set(parts)
        if missing:
            raise CardError(f"{path}: {lang} translation is missing {sorted(missing)}")

        if cloze:
            _check_cloze_faithful(sections_text, parts["text"], lang, path)
    return langs


def suspect_translations(card: "Card") -> list[str]:
    """Languages whose translation looks rewritten rather than translated.

    A translation carrying a code block its English side never had is the
    signature of a model that answered the question from its own knowledge
    instead of translating it — measured on a real batch, it marked
    corrupted cards and nothing else. It is reported rather than raised:
    the English card is still correct and must keep building. What it does
    block is shipping that language (see `build --lang`).
    """
    out = []
    english_len = len(card.question) + len(card.answer) if card.type == "qa" else len(card.text)
    for lang, parts in card.tr.items():
        for part, english in (("question", card.question), ("answer", card.answer)):
            if parts.get(part, "").count("```") > english.count("```"):
                out.append(lang)
                break
        else:
            # A translation far longer than its source is padding or, as
            # happened here, a second copy of the card pasted underneath by
            # a concurrent writer — invisible to the repeated-heading check
            # because the duplicate carries no heading of its own.
            if english_len and sum(map(len, parts.values())) > english_len * 1.6:
                out.append(lang)
    return out


_CLOZE_FULL_RE = re.compile(r"\{\{c(\d+)::(.*?)\}\}", re.DOTALL)
_NUMBER_RE = re.compile(r"\d+(?:[.,]\d+)*")


def _check_cloze_faithful(english: str, translated: str, lang: str, path: Path) -> None:
    """A translated cloze must test exactly what the English one tests.

    Prose inside a deletion may be translated — an answer you are meant to
    produce should be in the language you are studying in. What may not
    change is which deletions exist and the numbers inside them: a dropped
    deletion silently removes a probe, and a re-worded quantity teaches
    something false. Both were produced by translation models in practice,
    which is why this is enforced rather than asked for.
    """
    src = _CLOZE_FULL_RE.findall(english)
    dst = _CLOZE_FULL_RE.findall(translated)
    if not dst:
        raise CardError(f"{path}: {lang} cloze translation has no {{{{c1::...}}}} deletion")
    src_idx = sorted({i for i, _ in src})
    dst_idx = sorted({i for i, _ in dst})
    if src_idx != dst_idx:
        raise CardError(
            f"{path}: {lang} translation has deletions {dst_idx} but the English "
            f"card has {src_idx} — a translation may not add or drop a probe"
        )
    by_index: dict[str, str] = {}
    for i, text in dst:
        by_index[i] = by_index.get(i, "") + " " + text
    for i, text in src:
        want = set(_NUMBER_RE.findall(text))
        missing = sorted(want - set(_NUMBER_RE.findall(by_index.get(i, ""))))
        if missing:
            raise CardError(
                f"{path}: {lang} deletion c{i} lost the number(s) {missing} — "
                "quantities inside a deletion are the answer and must survive"
            )


def _split_qa(sections: dict[str, str], path: Path) -> tuple[str, str]:
    question, answer = sections.get("q", ""), sections.get("a", "")
    if not question or not answer:
        raise CardError(f"{path}: qa card body must be '## Q' section then '## A' section")
    return question, answer


def parse_card(path: str | Path) -> Card:
    path = Path(path)
    meta, body = _split_frontmatter(path.read_text(encoding="utf-8"), path)

    card_id = meta.get("id")
    if not isinstance(card_id, str) or not _ID_RE.match(card_id):
        raise CardError(f"{path}: invalid id {card_id!r} (want lowercase-hyphenated slug)")
    node = meta.get("node")
    if not isinstance(node, str) or not node:
        raise CardError(f"{path}: missing node")
    card_type = meta.get("type", "qa")
    if card_type not in CARD_TYPES:
        raise CardError(f"{path}: type must be one of {CARD_TYPES}, got {card_type!r}")
    tags = meta.get("tags", []) or []
    if not (isinstance(tags, list) and all(isinstance(t, str) for t in tags)):
        raise CardError(f"{path}: tags must be a list of strings")
    unknown = set(meta) - {"id", "node", "type", "tags", "source"}
    if unknown:
        raise CardError(f"{path}: unknown frontmatter keys {sorted(unknown)}")

    card = Card(
        id=card_id,
        node=node,
        type=card_type,
        path=path,
        tags=list(tags),
        source=str(meta.get("source", "") or ""),
    )
    try:
        preamble, sections = _sections(body)
    except CardError as exc:
        raise CardError(f"{path}: {exc}") from None
    if card_type == "qa":
        card.question, card.answer = _split_qa(sections, path)
        card.tr = _translations(sections, path, cloze=False)
    else:
        body = preamble
        card.tr = _translations(sections, path, cloze=True, sections_text=preamble)
        if not body:
            raise CardError(f"{path}: empty cloze body")
        if not _CLOZE_RE.search(body):
            raise CardError(f"{path}: cloze card has no {{{{c1::...}}}} deletion")
        card.text = body
    return card


def load_cards(cards_dir: str | Path) -> tuple[list[Card], list[str]]:
    """Parse every .md file under cards_dir. Returns (cards, errors) —
    one bad file never hides the rest."""
    cards: list[Card] = []
    errors: list[str] = []
    for path in sorted(Path(cards_dir).rglob("*.md")):
        try:
            cards.append(parse_card(path))
        except CardError as exc:
            errors.append(str(exc))
    return cards, errors


# A card written from a book must not need the book. These are the tells of
# one that does — "the book recommends", "as discussed above" — and the
# importer refuses them, because a reader reviewing in Anki has no book.
SOURCE_LEANING = (
    "书中", "本书", "作者建议", "作者认为", "如前所述", "前面提到", "上一节", "本节", "本章",
    "第一章", "第二章", "第三章", "第四章", "第五章", "第六章", "第七章", "第八章", "第九章",
    "the book", "this chapter", "as discussed", "as mentioned above", "see chapter",
    "earlier in this",
)
_CHAPTER_REF = re.compile(r"第\s*\d+\s*章|chapter\s+\d+", re.IGNORECASE)


def leans_on_source(text: str) -> str:
    """The first phrase that makes the card depend on its source, or ''."""
    low = text.lower()
    for phrase in SOURCE_LEANING:
        if phrase in low:
            return phrase
    m = _CHAPTER_REF.search(text)
    return m.group(0) if m else ""
