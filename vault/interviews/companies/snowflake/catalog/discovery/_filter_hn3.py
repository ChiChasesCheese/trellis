import json
import re
from pathlib import Path

D = Path("/Users/chizhang/Code/trellis/.claude/worktrees/snowflake-loop/vault/interviews/companies/snowflake/catalog/discovery/harvest")
rows = json.loads((D / "hn_2026-09-13.json").read_text(encoding="utf-8"))

SNOW = re.compile(r"\bsnowflake\b", re.I)
CTX = re.compile(r"interview|onsite|phone screen|leetcode|hackerrank|offer letter|rejected|recruiter call|coding round|system design round|hiring manager|screening", re.I)
WINDOW = 180


def near(text):
    for m in SNOW.finditer(text):
        s, e = max(0, m.start() - WINDOW), m.end() + WINDOW
        if CTX.search(text[s:e]):
            return text[max(0, m.start() - 250): m.end() + 250]
    return None


hits = []
for r in rows:
    text = r.get("text") or ""
    snippet = near(text)
    if snippet:
        hits.append((r, snippet))

hits.sort(key=lambda x: x[0]["created_at"], reverse=True)
print(f"proximity-filtered hits: {len(hits)}")
out_lines = []
for r, snippet in hits:
    out_lines.append("=" * 80)
    out_lines.append(f"{r['created_at'][:10]} {r['kind']} {r['url']}")
    out_lines.append(r["title"][:80])
    out_lines.append(snippet.replace("\n", " "))
(D.parent / "_hn_proximity_dump.txt").write_text("\n".join(out_lines), encoding="utf-8")
print("wrote _hn_proximity_dump.txt")
