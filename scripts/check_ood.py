"""Acceptance gate for the 20-minute OOD write-ups in vault/interviews/core/low-level-design/amazon/.

    python3 scripts/check_ood.py              # every oodNN-*.md
    python3 scripts/check_ood.py ood03 ood04  # some

A write-up passes when: the sections below appear in order and `## 来源` is the last one (the only place provenance may
appear — Chi, 2026-10-19: 「来源放最底下」); prose outside code is 3,000–7,500 characters (≈ 20 minutes); there is exactly
one ```python block under `## Python 骨架`, ≤ 170 lines, that runs with `python3 -I` and exits 0; there is a small
classDiagram; the plain-style rules (scripts/plain_style.py) hold for everything above `## 来源`; wikilinks resolve.
"""
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from plain_style import problems as style_problems  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "vault"
HERE = VAULT / "interviews/core/low-level-design/amazon"
SECTIONS = ["题目", "先问这几个问题", "核心对象", "主流程", "关键决策", "Python 骨架", "面试官加需求时",
            "并发与扩展", "常见错误", "30 秒复述", "来源"]
PROSE = (3000, 7500)
MAX_CODE = 170
FENCE = re.compile(r"^```.*?^```", re.S | re.M)
WIKILINK = re.compile(r"\[\[([^\]|#]+)")


def check(path: Path, names: set[str]) -> list[str]:
    text = path.read_text(encoding="utf-8")
    out: list[str] = []
    heads = re.findall(r"^## (.+?)\s*$", text, re.M)
    it = iter(SECTIONS)
    want = next(it)
    for h in heads:
        if want and h.startswith(want):
            want = next(it, None)
    if want:
        out.append(f"missing or out-of-order section: ## {want}")
    if not heads or not heads[-1].startswith("来源"):
        out.append("## 来源 must be the last section")
    body = text.split("\n## 来源", 1)[0]
    prose = FENCE.sub("", body)
    if not PROSE[0] <= len(prose) <= PROSE[1]:
        out.append(f"prose {len(prose)} chars outside {PROSE}")
    sk = body.split("## Python 骨架", 1)[-1].split("\n## ", 1)[0]
    code = re.findall(r"^```python\n(.*?)^```", sk, re.S | re.M)
    if len(code) != 1:
        out.append(f"{len(code)} python block(s) under ## Python 骨架; need exactly 1")
    else:
        lines = code[0].count("\n")
        if lines > MAX_CODE:
            out.append(f"skeleton {lines} lines > {MAX_CODE}")
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "skeleton.py"
            f.write_text(code[0], encoding="utf-8")
            p = subprocess.run([sys.executable, "-I", str(f)], capture_output=True, text=True, timeout=60)
            if p.returncode:
                err = (p.stderr or p.stdout).strip().splitlines()
                out.append(f"skeleton does not run: {err[-1] if err else p.returncode}")
    if "classDiagram" not in body:
        out.append("no mermaid classDiagram")
    out += style_problems(body)
    for link in WIKILINK.findall(text):
        if link.strip().rstrip("\\") not in names:
            out.append(f"dead wikilink [[{link}]]")
    return out


def main(argv: list[str]) -> int:
    names = {p.stem for p in VAULT.rglob("*.md")}
    files = sorted(HERE.glob("ood[0-9][0-9]-*.md"))
    if argv:
        files = [f for f in files if any(f.name.startswith(a) for a in argv)]
    bad = 0
    for f in files:
        found = check(f, names)
        print(f"{'FAIL' if found else 'ok  '} {f.name}" + "".join(f"\n       - {p}" for p in found))
        bad += bool(found)
    print(f"{len(files) - bad}/{len(files)} write-up(s) pass")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
