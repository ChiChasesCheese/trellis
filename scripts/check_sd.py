"""Acceptance gate for the reported system-design write-ups under vault/interviews/core/system-design/.

    python3 scripts/check_sd.py                 # every sdNN-*.md under vault/interviews/core/system-design/
    python3 scripts/check_sd.py sd01            # one

A write-up passes when it has every required section in order, no provenance anywhere (study links only in 延伸阅读),
at least three mermaid diagrams that fit the page (one architecture flowchart, one sequence diagram),
9,000+ characters of prose outside code, at least three deep dives, self-check answers in <details>,
wikilinks that resolve to a note in the vault, and the plain-style rules of proposals/WRITING_RULES.md
(scripts/plain_style.py).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from plain_style import problems as style_problems  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "vault"
HERE = VAULT / "interviews/core/system-design"
SECTIONS = ["题目", "澄清问题", "需求", "容量估算", "核心实体与 API", "高层架构", "深挖",
            "Staff 视角：权衡、故障与演进", "面试官追问", "60 分钟怎么分配", "自测", "延伸阅读"]
FORBIDDEN = ["我验证过", "对拍", "如上所述"]
MIN_PROSE = 9000
FENCE = re.compile(r"^```.*?^```", re.S | re.M)
WIKILINK = re.compile(r"\[\[([^\]|#]+)")


def note_names() -> set[str]:
    return {p.stem for p in VAULT.rglob("*.md")}


def check(path: Path, names: set[str]) -> list[str]:
    text = path.read_text(encoding="utf-8")
    problems: list[str] = []
    heads = re.findall(r"^## (.+?)\s*$", text, re.M)
    want = iter(SECTIONS)
    pending = next(want)
    for h in heads:
        if pending and h.startswith(pending):
            pending = next(want, None)
    if pending:
        problems.append(f"missing or out-of-order section: ## {pending}")
    mermaid = [re.sub(r"^\s*%%.*\n", "", m, flags=re.M)        # drop init directives before reading the type
               for m in re.findall(r"^```mermaid\n(.*?)^```", text, re.S | re.M)]
    if len(mermaid) < 3:
        problems.append(f"{len(mermaid)} mermaid diagram(s); need >= 3")
    if not any(m.lstrip().startswith(("flowchart", "graph")) for m in mermaid):
        problems.append("no architecture flowchart")
    if not any(m.lstrip().startswith("sequenceDiagram") for m in mermaid):
        problems.append("no sequenceDiagram")
    prose = FENCE.sub("", text)
    if len(prose) < MIN_PROSE:
        problems.append(f"prose {len(prose)} chars < {MIN_PROSE}")
    tail = text.split("\n## 延伸阅读", 1)[-1]
    if not re.search(r"https?://|\[\[", tail):
        problems.append("'## 延伸阅读' has no link")
    problems += style_problems(text)
    deep = text.split("## 深挖", 1)[-1].split("\n## ", 1)[0]
    if len(re.findall(r"^### ", deep, re.M)) < 3:
        problems.append("fewer than 3 ### deep dives")
    if "<details>" not in text.split("## 自测", 1)[-1]:
        problems.append("自测 has no <details> answers")
    for word in FORBIDDEN:
        if word in prose:
            problems.append(f"forbidden phrase: {word}")
    for link in WIKILINK.findall(text):
        if link.strip() not in names:
            problems.append(f"dead wikilink [[{link}]]")
    return problems


def main(argv: list[str]) -> int:
    names = note_names()
    files = sorted(HERE.rglob("sd[0-9][0-9]-*.md"))
    if argv:
        files = [f for f in files if any(f.name.startswith(a) for a in argv)]
    failed = 0
    for f in files:
        found = check(f, names)
        print(f"{'FAIL' if found else 'ok  '} {f.name}" + "".join(f"\n       - {p}" for p in found))
        failed += bool(found)
    print(f"{len(files) - failed}/{len(files)} write-up(s) pass")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
