"""The 240 problems of Blind 75 / NeetCode 150 / LeetCode Hot 100 / Top Interview 150, one line each, for picking the
core problem (核心题) of a knowledge point.

    python3 scripts/core_lists.py               # all 240: LC n, Chinese title, topic tags, lists
    python3 scripts/core_lists.py union-find    # only lines whose tags or title contain the word
"""
import json
import sys
from pathlib import Path

CAT = Path(__file__).resolve().parents[1] / "research/companies/tiktok/catalog"
LISTS = ("Blind 75", "NeetCode 150", "LeetCode Hot 100", "Top Interview 150")
lists = json.loads((CAT / "other_lists.json").read_text(encoding="utf-8"))
meta = json.loads((CAT / "lc_meta.json").read_text(encoding="utf-8"))
want = " ".join(sys.argv[1:]).lower()
for n in sorted({int(x) for name in LISTS for x in lists[name]}):
    m = meta[str(n)]
    on = [name for name in LISTS if n in {int(x) for x in lists[name]}]
    line = f"LC {n} {m['zh']} | {', '.join(m['tags'])} | {'、'.join(on)}"
    if not want or want in line.lower():
        print(line)
