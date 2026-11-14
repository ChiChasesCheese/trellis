"""Turn ```svg fences into bare <svg> blocks, so Obsidian draws them as Anki does (Chi, 2026-11-14).

    uv run python scripts/svg_unfence.py [paths…]     # default: every .md under vault/

A bare block keeps a blank line before and after and none inside: Obsidian ends an HTML block at a blank line.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FENCE = re.compile(r"^```svg[ \t]*\n(.*?)^```[ \t]*$", re.S | re.M)


def unfence(text: str) -> str:
    def bare(m: re.Match) -> str:
        body = "\n".join(line for line in m.group(1).strip().splitlines() if line.strip())
        return body
    return FENCE.sub(bare, text)


def main() -> int:
    paths = [Path(p) for p in sys.argv[1:]] or list((ROOT / "vault").rglob("*.md"))
    changed = 0
    for p in paths:
        t = p.read_text(encoding="utf-8", errors="ignore")
        if "```svg" in t:
            n = unfence(t)
            if n != t:
                p.write_text(n, encoding="utf-8")
                changed += 1
    print(f"unfenced svg in {changed} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
