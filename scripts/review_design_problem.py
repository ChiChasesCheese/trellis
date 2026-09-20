"""What the orchestrator reads before accepting a design problem (BUILD.md §5).

    uv run python scripts/review_design_problem.py <slug> [...]

Prints, per problem: the gate result, every line of the capacity estimate (to
re-derive), each card's question, and any figure that appears in a card but
not in the article — a number a card did not inherit is a number nobody checked.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "vault/domains/system-design"
NUMBER = re.compile(r"\d[\d,]*\.?\d*\s?(?:%|[KMGTP]i?B|QPS|ms|TB|GB|MB|KB|亿|万|billion|million)?")


def figures(text: str) -> set[str]:
    return {re.sub(r"[\s,]", "", m.group(0)) for m in NUMBER.finditer(text) if len(m.group(0).strip()) > 1}


def main(slugs: list[str]) -> int:
    for slug in slugs:
        article = BASE / f"readings/problems/solution-{slug}.md"
        cards = sorted((BASE / "cards/problems").glob(f"problems-{slug}-*.md"))
        print(f"\n{'=' * 8} {slug}: {len(cards)} card(s), article {len(article.read_text(encoding='utf-8')) if article.exists() else 0} chars")
        if not article.exists():
            continue
        text = article.read_text(encoding="utf-8")
        est = text.split("## 容量估算", 1)[1].split("\n## ", 1)[0] if "## 容量估算" in text else ""
        print("--- capacity estimate (re-derive these) ---")
        for line in est.strip().splitlines():
            if re.search(r"\d", line):
                print("  " + line.strip()[:260])
        in_article = figures(text)
        print("--- cards ---")
        for c in cards:
            body = c.read_text(encoding="utf-8")
            q = body.split("## Q", 1)[1].split("## A", 1)[0].strip().replace("\n", " ")
            english = body.split("## Q zh", 1)[0]
            orphan = sorted(f for f in figures(english.split("---", 2)[2]) - in_article
                            if re.search(r"[%A-Za-z亿万]", f) or len(f) >= 3)
            print(f"  [{c.stem.removeprefix('problems-' + slug + '-')}] {q[:150]}")
            if orphan:
                print(f"      figures not in the article: {orphan[:8]}")
    leaves = subprocess.run(["uv", "run", "python", "scripts/check_design_problems.py", "--all"],
                            cwd=ROOT, capture_output=True, text=True).stdout.splitlines()
    print("\n--- gate ---")
    for line in leaves:
        if any(line.rstrip().endswith("." + s) or f".{s}\n" in line + "\n" for s in slugs) or "pass" in line:
            print("  " + line)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
