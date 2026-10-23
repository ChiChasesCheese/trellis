#!/usr/bin/env python3
"""Resume reddit-post full-text fetch after the initial run hit a sustained 429 wall.
Recomputes the same candidate set from the per-sub search JSON already on disk, skips
ids already saved, and fetches the rest with a longer external delay (on top of
harvest.reddit_post's own internal 4-try backoff)."""
import json
import re
import sys
import time
from pathlib import Path

TOOLS = Path("/Users/chizhang/Code/trellis/.claude/worktrees/snowflake-loop/vault/interviews/companies/snowflake/tools")
sys.path.insert(0, str(TOOLS))
import harvest  # noqa: E402

OUT = Path("/Users/chizhang/Code/trellis/.claude/worktrees/snowflake-loop/vault/interviews/companies/snowflake/catalog/discovery")
HARVEST_DIR = OUT / "harvest"
LOG = OUT / "_resume_posts.log"

SUBS = ["leetcode", "cscareerquestions", "csMajors", "ExperiencedDevs", "snowflake", "dataengineering"]
STAMP = "2026-09-13"

RELEVANT_RE = re.compile(r"snowflake", re.I)
CTX_RE = re.compile(r"interview|\boa\b|onsite|screen|offer|assessment|hackerrank|codesignal|chakra", re.I)


def log(msg: str) -> None:
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def main() -> None:
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 56  # 60 - 4 already saved
    delay = float(sys.argv[2]) if len(sys.argv) > 2 else 6.0

    all_hits_by_sub = {}
    for sub in SUBS:
        path = HARVEST_DIR / f"reddit_{sub}_{STAMP}.json"
        all_hits_by_sub[sub] = json.loads(path.read_text(encoding="utf-8"))

    candidates = []
    for sub, rows in all_hits_by_sub.items():
        for h in rows:
            title = h.get("title", "")
            if RELEVANT_RE.search(title) and CTX_RE.search(title):
                candidates.append(h)
    candidates.sort(key=lambda h: h.get("published", ""), reverse=True)
    candidates = candidates[:60]

    posts_path = HARVEST_DIR / f"reddit_posts_{STAMP}.json"
    posts = json.loads(posts_path.read_text(encoding="utf-8")) if posts_path.exists() else []
    done = {p["id"] for p in posts}
    log(f"already have {len(done)} posts; {len(candidates)} total candidates")

    todo = [h for h in candidates if h["id"] not in done][:cap]
    log(f"fetching {len(todo)} more (cap={cap}, delay={delay}s)")

    ok = 0
    for i, h in enumerate(todo, 1):
        try:
            p = harvest.reddit_post(h["sub"], h["id"])
            p["published"] = h.get("published", "")
            p["query"] = h.get("query", "")
            posts.append(p)
            ok += 1
            log(f"  [{i}/{len(todo)}] OK {h['sub']}/{h['id']} body={len(p['body'])} comments={len(p['comments'])}")
        except Exception as exc:  # noqa: BLE001
            log(f"  [{i}/{len(todo)}] FAIL {h['sub']}/{h['id']}: {exc}")
        if i % 5 == 0 or i == len(todo):
            posts_path.write_text(json.dumps(posts, ensure_ascii=False, indent=1), encoding="utf-8")
        time.sleep(delay)

    posts_path.write_text(json.dumps(posts, ensure_ascii=False, indent=1), encoding="utf-8")
    log(f"DONE: total saved posts now {len(posts)} (this run: {ok}/{len(todo)} ok)")


if __name__ == "__main__":
    main()
