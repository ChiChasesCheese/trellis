"""List bullets whose first words cannot serve as a phrase to recite from.

    uv run python research/hello-interview/phrase_todo.py [--group N]   # N of 3, by file; prints path, then the bullets
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from trellis import build as B  # noqa: E402

ROOTS = ["vault/domains/python/cards", "vault/domains/bagu/cards", "vault/domains/hello-interview/cards", "vault/interviews/core/design-questions",
         "vault/domains/hello-interview/premium/bodies"]


def bullets(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    if "## A" not in text:
        return []
    answer = re.sub(r"```.*?```", "", text.split("## A", 1)[1], flags=re.S)
    answer = re.sub(r"\[\[[^\]|]*\|([^\]]*)\]\]", r'<span class="ref">\1</span>', answer)
    out = []
    for line in answer.split("\n"):
        m = re.match(r"^(?:[-*+]|\d+\.)\s+(.*)$", line)
        if m:
            head, rest = B._head(m.group(1))
            if B._width(head) > B.PHRASE_MAX or (not rest and B._width(head) > 20):
                out.append(m.group(1))
    return out


def main() -> int:
    group = int(sys.argv[2]) if len(sys.argv) > 2 else None
    files = [f for r in ROOTS for f in sorted((ROOT / r).rglob("*.md"))]
    todo = [(f, b) for f in files if (b := bullets(f))]
    total = 0
    for i, (f, items) in enumerate(todo):
        if group is not None and i % 3 != group - 1:
            continue
        total += len(items)
        print(f.relative_to(ROOT))
        for x in items:
            print("  -", x)
    print(f"{total} bullets in {len(todo)} files overall group view")
    return 0


if __name__ == "__main__":
    sys.exit(main())
