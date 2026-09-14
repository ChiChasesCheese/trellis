#!/usr/bin/env python3
import json
import sys
import time
from pathlib import Path

TOOLS = Path("/Users/chizhang/Code/trellis/.claude/worktrees/snowflake-loop/vault/interviews/companies/snowflake/tools")
sys.path.insert(0, str(TOOLS))
import harvest  # noqa: E402

OUT = Path("/Users/chizhang/Code/trellis/.claude/worktrees/snowflake-loop/vault/interviews/companies/snowflake/catalog/discovery")
HARVEST_DIR = OUT / "harvest"
STAMP = "2026-09-13"

HN_QUERIES = [
    "snowflake interview",
    "snowflake onsite",
    "snowflake hiring engineer",
    "snowflake interview process",
]


def main():
    hn_rows = []
    seen_hn = set()
    for q in HN_QUERIES:
        for tags in ("comment", "story"):
            try:
                rows = harvest.hn_search(q, tags=tags)
            except Exception as exc:  # noqa: BLE001
                print(f"! hn {q!r} {tags}: {exc}")
                rows = []
            new = 0
            for r in rows:
                if r["id"] not in seen_hn:
                    seen_hn.add(r["id"])
                    hn_rows.append(r)
                    new += 1
            print(f"hn {q!r} ({tags}) -> {len(rows)} (new {new}, total {len(hn_rows)})")
            time.sleep(1.0)
    hn_path = HARVEST_DIR / f"hn_{STAMP}.json"
    hn_path.write_text(json.dumps(hn_rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"== hn done: {len(hn_rows)} rows -> {hn_path.name}")


if __name__ == "__main__":
    main()
