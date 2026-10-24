"""Gate for tiktok-lc cards: every python block compiles and runs its definitions, functions carry type hints,
no forbidden narration, ids and nodes well-formed.

    uv run python research/companies/tiktok/tools/gate_cards.py [card files ...]   # default: the whole deck
"""
import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
CARDS = ROOT / "vault/interviews/core/leetcode/tiktok/cards"
DRILL = ROOT / "vault/interviews/core/leetcode/tiktok-drill/cards"
BLOCK = re.compile(r"```python\n(.*?)```", re.S)
FORBIDDEN = ["本题", "这道题", "本文", "如上所述", "见上", "对拍", "验证过程", "随机测试", "我测了"]
PRELUDE = ("from __future__ import annotations\nimport bisect, collections, functools, heapq, itertools, math, "
           "operator, random, re, string, sys\nfrom collections import *\nfrom functools import *\n"
           "from heapq import *\nfrom itertools import *\nfrom bisect import *\nfrom math import inf\n"
           "from typing import *\nclass ListNode:\n    def __init__(self, val=0, next=None):\n"
           "        self.val, self.next = val, next\nclass TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n"
           "        self.val, self.left, self.right = val, left, right\nclass Node:\n    def __init__(self, val=0, *a, **k):\n"
           "        self.val = val\n")


def problems(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    out = []
    if not re.search(r"^id: tlc-[a-z0-9-]+$", text, re.M):
        out.append("id must start with tlc-")
    for word in FORBIDDEN:
        if word in text:
            out.append(f"forbidden word {word!r}")
    for i, block in enumerate(BLOCK.findall(text), 1):
        if "..." in block or "# usage" in block.lower():
            continue  # a fragment, not a full solution
        try:
            tree = ast.parse(block)
        except SyntaxError as e:
            out.append(f"python block {i}: {e}")
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("_") and node.name != "__init__":
                args = [a for a in node.args.args if a.arg not in ("self", "cls")]
                if any(a.annotation is None for a in args) or node.returns is None:
                    out.append(f"python block {i}: {node.name}() needs type hints")
        try:
            exec(compile(PRELUDE + block, str(path), "exec"), {"__name__": "gate"})
        except Exception as e:  # noqa: BLE001 - any failure to define the solution is a defect
            out.append(f"python block {i}: {type(e).__name__}: {e}")
    return out


def main(argv: list[str]) -> int:
    files = [Path(a).resolve() for a in argv] or sorted([*CARDS.rglob("*.md"), *DRILL.rglob("*.md")])
    bad = 0
    for f in files:
        for p in problems(f):
            bad += 1
            print(f"{f.relative_to(ROOT)}: {p}")
    print(f"{len(files)} card(s), {bad} problem(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
