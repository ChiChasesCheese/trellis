"""Keep the code shown in an LLD solution article identical to the code that is tested.

    uv run python scripts/lld_embed_code.py <slug> [...]      # rewrite the managed blocks
    uv run python scripts/lld_embed_code.py --check <slug>    # exit 1 if any block is stale

In the article, write a marker pair and nothing between it:

    %% code:begin solution.py %%
    %% code:end %%

The script fills it with the file, fenced as python. An optional symbol narrows it to one
top-level class or function:  %% code:begin solution.py ParkingLot %%
"""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "vault/domains/low-level-design"
BLOCK = re.compile(r"(%% code:begin (\S+?)(?: (\w+))? %%\n)(.*?)(%% code:end %%)", re.S)


def snippet(path: Path, symbol: str | None) -> str:
    source = path.read_text(encoding="utf-8")
    if not symbol:
        return source.rstrip("\n")
    lines = source.splitlines()
    for node in ast.parse(source).body:
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == symbol:
            start = min([node.lineno] + [d.lineno for d in node.decorator_list]) - 1
            return "\n".join(lines[start:node.end_lineno])
    raise SystemExit(f"{path}: no top-level class or function named {symbol}")


def render(slug: str, text: str) -> str:
    def fill(m: re.Match) -> str:
        body = snippet(BASE / "problems" / slug / m.group(2), m.group(3))
        return f"{m.group(1)}```python\n{body}\n```\n{m.group(5)}"
    return BLOCK.sub(fill, text)


def main(argv: list[str]) -> int:
    check = "--check" in argv
    stale = 0
    for slug in [a for a in argv if not a.startswith("--")]:
        article = BASE / "readings/problems" / f"solution-{slug}.md"
        text = article.read_text(encoding="utf-8")
        new = render(slug, text)
        if new != text:
            stale += 1
            if check:
                print(f"stale: {article.name}")
            else:
                article.write_text(new, encoding="utf-8")
                print(f"updated: {article.name}")
    return 1 if check and stale else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
