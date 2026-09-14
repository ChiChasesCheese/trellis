#!/usr/bin/env python3
"""Second retry pass for reddit-post ids that failed with 429 in _resume_posts.py, this time
with a longer external delay. Parses failed (sub,id) pairs straight from _resume_posts.log."""
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
LOG = OUT / "_retry_failed.log"
STAMP = "2026-09-13"

FAIL_RE = re.compile(r"FAIL (\S+)/(\S+): ")


def log(msg: str) -> None:
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def main() -> None:
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 34
    delay = float(sys.argv[2]) if len(sys.argv) > 2 else 9.0

    resume_log = (OUT / "_resume_posts.log").read_text(encoding="utf-8")
    failed = []
    seen = set()
    for m in FAIL_RE.finditer(resume_log):
        sub, pid = m.group(1), m.group(2)
        if pid not in seen:
            seen.add(pid)
            failed.append((sub, pid))

    posts_path = HARVEST_DIR / f"reddit_posts_{STAMP}.json"
    posts = json.loads(posts_path.read_text(encoding="utf-8")) if posts_path.exists() else []
    done = {p["id"] for p in posts}
    todo = [(sub, pid) for sub, pid in failed if pid not in done][:cap]
    log(f"{len(failed)} distinct failed ids, {len(todo)} still missing, retrying up to cap={cap}")

    ok = 0
    for i, (sub, pid) in enumerate(todo, 1):
        try:
            p = harvest.reddit_post(sub, pid)
            p["published"] = ""
            p["query"] = "retry"
            posts.append(p)
            ok += 1
            log(f"  [{i}/{len(todo)}] OK {sub}/{pid} body={len(p['body'])} comments={len(p['comments'])}")
        except Exception as exc:  # noqa: BLE001
            log(f"  [{i}/{len(todo)}] FAIL {sub}/{pid}: {exc}")
        if i % 5 == 0 or i == len(todo):
            posts_path.write_text(json.dumps(posts, ensure_ascii=False, indent=1), encoding="utf-8")
        time.sleep(delay)

    posts_path.write_text(json.dumps(posts, ensure_ascii=False, indent=1), encoding="utf-8")
    log(f"DONE: total saved posts now {len(posts)} (this run: {ok}/{len(todo)} ok)")


if __name__ == "__main__":
    main()
