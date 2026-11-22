"""Mechanical format fixes on vault cards (## Q / ## A markdown). Dry run by default.

    uv run python scripts/card_normalize.py <rule>[,<rule>…] <domain> [<domain> …]           # report what would change
    uv run python scripts/card_normalize.py fold-source,dedupe-label k8s ai-eng --apply     # rewrite the files
    then: uv run python scripts/anki_refresh.py <domain>                                     # push the edits to Anki

Rules (each is idempotent: a second run changes nothing):
- fold-source    the last line `**出处：** …` becomes a folded block (tap to open), so the citation stays but leaves the body
- fold-tail      `**面试官在考什么：**` and `**适合配哪类故事：**` paragraphs move into one folded block (with 出处 if present)
- dedupe-label   question header `**Title · 摘要**｜摘要 · 必会` → `**Title**｜摘要 · 必会` when the kind is said twice
- self-reference 本卡 → 上面 (a card must not talk about itself; the learner sees one side at a time)
- drop-no-lc     removes the line `**对应 LeetCode：** 无直接对应的题…` (it says nothing)

Built 2026-11-21 from the deck audit (scripts/deck_audit.py); add a rule here when an audit finds a new mechanical defect.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
FOLD = '<details class="pt" markdown="1"><summary>{summary}</summary>\n\n{body}\n\n</details>'
SOURCE = re.compile(r"^\*\*出处：\*\*\s*(.+)$")
TAIL = re.compile(r"^\*\*(面试官在考什么|适合配哪类故事)：\*\*")


def split_card(text: str) -> tuple[str, str, str] | None:
    m = re.match(r"(\A---\n.*?\n---\n)(.*?)(^## A\n.*)\Z", text, re.S | re.M)
    return (m.group(1), m.group(2), m.group(3)) if m else None


def paragraphs(answer: str) -> list[str]:
    """Blank-line separated blocks; code fences and existing <details> stay whole."""
    blocks, cur, fence, depth = [], [], False, 0
    for line in answer.split("\n"):
        if line.startswith("```"):
            fence = not fence
        depth += line.count("<details") - line.count("</details>")
        if not line.strip() and not fence and depth == 0:
            if cur:
                blocks.append("\n".join(cur))
                cur = []
        else:
            cur.append(line)
    if cur:
        blocks.append("\n".join(cur))
    return blocks


def fold_source(front: str, q: str, a: str) -> tuple[str, str]:
    if "<summary>出处</summary>" in a or "· 出处</summary>" in a:
        return q, a
    blocks = paragraphs(a)
    if blocks and SOURCE.match(blocks[-1].strip()):
        blocks[-1] = FOLD.format(summary="出处", body=SOURCE.match(blocks[-1].strip()).group(1))
        return q, "\n\n".join(blocks) + "\n"
    return q, a


def fold_tail(front: str, q: str, a: str) -> tuple[str, str]:
    if "<summary>面试官看什么" in a:
        return q, a
    blocks = paragraphs(a)
    head, tail, source = [], [], None
    for b in blocks:
        s = b.strip()
        if TAIL.match(s):
            tail.append(s)
        elif SOURCE.match(s) or "<summary>出处</summary>" in s:
            source = SOURCE.match(s).group(1) if SOURCE.match(s) else re.search(r"</summary>\s*(.*?)\s*</details>", s, re.S).group(1)
        else:
            head.append(b)
    if not tail:
        return q, a
    body = "\n\n".join(tail + ([f"**出处：** {source}"] if source else []))
    summary = "面试官看什么 · 配哪类故事" + (" · 出处" if source else "")
    return q, "\n\n".join(head + [FOLD.format(summary=summary, body=body)]) + "\n"


def dedupe_label(front: str, q: str, a: str) -> tuple[str, str]:
    def fix(m: re.Match) -> str:
        title, kind, rest = m.group(1), m.group(2), m.group(3)
        return f"**{title}**｜{kind}{rest}"
    return re.sub(r"^\*\*(.+?) · ([^*·｜]+)\*\*｜\2( · [^\n]*)?$", fix, q, count=1, flags=re.M), a


def self_reference(front: str, q: str, a: str) -> tuple[str, str]:
    return q.replace("本卡", "上面"), a.replace("本卡", "上面")


def drop_no_lc(front: str, q: str, a: str) -> tuple[str, str]:
    return q, re.sub(r"\n*^\*\*对应 LeetCode：\*\* 无直接对应的题[^\n]*$", "", a, flags=re.M)


RULES = {"fold-source": fold_source, "fold-tail": fold_tail, "dedupe-label": dedupe_label,
         "self-reference": self_reference, "drop-no-lc": drop_no_lc}


def card_files(domain: str) -> list[Path]:
    sk = yaml.safe_load((ROOT / f"skeleton/{domain}.yaml").read_text(encoding="utf-8"))
    return sorted((ROOT / "vault" / sk["vault"] / "cards").rglob("*.md"))


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    apply = "--apply" in sys.argv
    if len(args) < 2 or any(r not in RULES for r in args[0].split(",")):
        print(__doc__)
        return 2
    rules = args[0].split(",")
    for domain in args[1:]:
        changed = 0
        files = card_files(domain)
        for f in files:
            text = f.read_text(encoding="utf-8")
            parts = split_card(text)
            if not parts:
                continue
            front, q, a = parts
            for r in rules:
                q, a = RULES[r](front, q, a)
            new = front + q + a
            if new != text:
                changed += 1
                if apply:
                    f.write_text(new, encoding="utf-8")
        print(f"{domain}: {changed} of {len(files)} cards {'rewritten' if apply else 'would change'} ({','.join(rules)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
