"""Does every Hello Interview chapter have its summary, exam and beyond cards, with every section accounted for?

    uv run python research/hello-interview/check_course.py                 # all pages, one line each, then totals
    uv run python research/hello-interview/check_course.py --group FILE    # only the pages in a group file; exit 1 on a gap

A page is ok when its coverage ledger names every `##` heading and every `###` heading with more than MIN_H3 characters
beneath it, each mapped to summary cards that exist or to a stated skip, and it has at least the minimum number of cards of
each kind. Page text and ledgers stay in sources/local/; this prints only headings that are missing.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / "sources/local/hello-interview/premium"
CARDS = ROOT / "vault/domains/hello-interview/cards"
BASE = "https://www.hellointerview.com/learn/"
MIN_H3 = 1200
SHORT_PAGE = 5000
MIN_SUMMARY = 60
LEANS = re.compile(r"页面|原文|本章|这一章|这一节|本节|课程里|上面|前面提到")


def headings(text: str) -> list[str]:
    """`##` headings, plus `###` headings long enough to carry their own material."""
    marks = list(re.finditer(r"^(#{1,6}) (.+)$", text, re.M))
    out = []
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        lvl = len(m.group(1))
        if lvl == 2 or (lvl == 3 and end - m.end() > MIN_H3):
            out.append(m.group(2).strip())
    return out


def card_index() -> dict[str, dict[str, list[str]]]:
    """leaf -> id list, for every card in the domain."""
    idx: dict[str, list[str]] = {}
    ids = set()
    for f in CARDS.rglob("*.md"):
        t = f.read_text(encoding="utf-8")
        i, n = re.search(r"^id: (\S+)$", t, re.M), re.search(r"^node: (\S+)$", t, re.M)
        if i and n:
            idx.setdefault(n.group(1), []).append(i.group(1))
            ids.add(i.group(1))
    return {"leaf": idx, "ids": ids}  # type: ignore[return-value]


def leaks(leaf: str, tid_cards: Path) -> list[str]:
    """Cards of this page that lean on a source the reader does not have, or that are too thin to teach."""
    probs = []
    for f in tid_cards.glob("*.md"):
        text = f.read_text(encoding="utf-8")
        hit = LEANS.search(text.split("---", 2)[-1])
        if hit:
            probs.append(f"{f.stem}: says {hit.group(0)}")
        if re.search(r"-n\d+-", f.stem):
            answer = re.sub(r"```.*?```", "", text.split("## A", 1)[-1], flags=re.S)
            if len(re.findall(r"[\u4e00-\u9fff]", answer)) < MIN_SUMMARY:
                probs.append(f"{f.stem}: thin summary")
    return probs


def check(leaf: str, stem: str, cards: dict) -> list[str]:
    page = LOCAL / "pages" / f"{stem}.md"
    if not page.exists():
        return ["page not fetched"]
    text = page.read_text(encoding="utf-8")
    short = len(text) < SHORT_PAGE
    probs = []
    lmin = {"notes": 1 if short else 3, "exam": 0 if short else 1, "beyond": 0 if short else 1}
    for kind, least in lmin.items():
        have = len(cards["leaf"].get(f"{leaf}.{kind}", []))
        if have < least:
            probs.append(f"{kind} {have}<{least}")
    tid, section, page_id = leaf.split(".")
    probs += leaks(leaf, CARDS / "premium" / tid / section / page_id)
    ledger = LOCAL / "coverage" / f"{stem}.json"
    if not ledger.exists():
        return probs + ["no coverage ledger"]
    sections = json.loads(ledger.read_text(encoding="utf-8"))["sections"]
    for h in headings(text):
        v = sections.get(h)
        if v is None:
            probs.append(f"missing section: {h}")
        elif isinstance(v, str):
            if not v.startswith("skip:"):
                probs.append(f"bad value for: {h}")
        else:
            missing = [c for c in v if c not in cards["ids"]]
            if not v or missing:
                probs.append(f"no such card under {h}: {missing}")
    return probs


def all_pages() -> list[tuple[str, str]]:
    out = []
    for p in json.loads((ROOT / "research/hello-interview/pages.json").read_text(encoding="utf-8")):
        tid = "sd" if p["track"] == "system-design" else "lld"
        out.append((f"{tid}.{p['section'] or p['page']}.{p['page']}", p["url"].replace(BASE, "").replace("/", "__")))
    return out


def main() -> int:
    if len(sys.argv) > 2 and sys.argv[1] == "--group":
        pages = [tuple(x.split()) for x in Path(sys.argv[2]).read_text(encoding="utf-8").splitlines() if x.strip()]
    else:
        pages = all_pages()
    cards = card_index()
    done = 0
    totals = {"notes": 0, "exam": 0, "beyond": 0}
    for leaf, stem in pages:
        probs = check(leaf, stem, cards)
        for k in totals:
            totals[k] += len(cards["leaf"].get(f"{leaf}.{k}", []))
        done += not probs
        print(f"{'ok ' if not probs else 'GAP'} {leaf}" + ("" if not probs else "  " + "; ".join(probs[:6])))
    print(f"{done}/{len(pages)} pages ok; cards {totals}")
    return 0 if done == len(pages) else 1


if __name__ == "__main__":
    sys.exit(main())
