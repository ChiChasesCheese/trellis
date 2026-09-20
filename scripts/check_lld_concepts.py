"""Acceptance gate for the concept layer of low-level-design (everything outside `problems`).

    uv run python scripts/check_lld_concepts.py method oop        # branches
    uv run python scripts/check_lld_concepts.py --all

A branch is done when every leaf has 4–8 cards and every card is Chinese-native (no translation
sections), has a `step` unique within its leaf, carries no Java, and every ```python block in it parses.
"""

from __future__ import annotations

import ast
import re
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from trellis.project import load_project  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CJK = re.compile(r"[一-鿿]")
JAVA = re.compile(r"```java|\bpublic (?:class|static|void|interface)\b|\bprivate final\b|@Override|\bimplements\b|"
                  r"\bsynchronized\b|System\.out|\bnew [A-Z]\w*\(|\bvolatile\b|\bextends\b")
FENCE = re.compile(r"```(\w*)\n(.*?)```", re.S)
MIN_CARDS, MAX_CARDS = 4, 8


def check_card(card) -> list[str]:
    out = []
    text = "\n".join([card.question, card.answer, card.text])
    if not CJK.search(card.question or card.text):
        out.append("the question is not Chinese")
    if len(CJK.findall(text)) / max(1, len(re.sub(r"```.*?```", "", text, flags=re.S))) < 0.3:
        out.append("the prose is not predominantly Chinese")
    if card.tr:
        out.append("carries a translation section; this domain is Chinese-native")
    if card.step is None:
        out.append("no step")
    m = JAVA.search(text)
    if m:
        out.append(f"Java in the card ({m.group(0)!r}); this deck is Python")
    for lang, code in FENCE.findall(text):
        if lang in ("python", "py"):
            try:
                ast.parse(textwrap.dedent(code))
            except SyntaxError as exc:
                out.append(f"a python block does not parse: {exc.msg} (line {exc.lineno})")
        elif lang == "" and re.search(r"^\s*(def|class|import|from) ", code, re.M):
            out.append("a code block with Python in it has no `python` language tag")
    return out


def main(argv: list[str]) -> int:
    project = load_project(ROOT, "low-level-design")
    roots = [r.id for r in project.skeleton.roots if r.id != "problems"]
    wanted = roots if argv == ["--all"] else argv
    by_leaf: dict[str, list] = {}
    for c in project.cards:
        by_leaf.setdefault(c.node, []).append(c)
    failed = 0
    for branch in wanted:
        if branch not in roots:
            print(f"FAIL {branch}: not a concept branch ({', '.join(roots)})")
            failed += 1
            continue
        problems = [e for e in project.card_errors if f"/cards/{branch}/" in e]
        n_cards = 0
        for leaf in project.skeleton.leaves():
            if not (leaf.id == branch or leaf.id.startswith(branch + ".")):
                continue
            cards = by_leaf.get(leaf.id, [])
            n_cards += len(cards)
            if not MIN_CARDS <= len(cards) <= MAX_CARDS:
                problems.append(f"{leaf.id}: {len(cards)} card(s), want {MIN_CARDS}–{MAX_CARDS}")
            for c in cards:
                problems += [f"{c.id}: {p}" for p in check_card(c)]
        print(f"{'FAIL' if problems else 'ok  '} {branch} ({n_cards} cards)" + "".join(f"\n       - {p}" for p in problems[:40])
              + (f"\n       … and {len(problems) - 40} more" if len(problems) > 40 else ""))
        failed += bool(problems)
    print(f"{len(wanted) - failed}/{len(wanted)} branch(es) pass")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
