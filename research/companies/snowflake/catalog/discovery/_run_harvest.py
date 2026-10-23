#!/usr/bin/env python3
"""One-shot orchestration for the Snowflake harvest. Not part of the shared tool;
lives in discovery/ scratch space, imports harvest.py functions directly so we control
pacing/dedup/checkpointing across the whole matrix in one process."""
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
HARVEST_DIR.mkdir(parents=True, exist_ok=True)
LOG = OUT / "_run_harvest.log"

SUBS = ["leetcode", "cscareerquestions", "csMajors", "ExperiencedDevs", "snowflake", "dataengineering"]
QUERIES = [
    "snowflake interview",
    "snowflake oa",
    "snowflake online assessment",
    "snowflake onsite",
    "snowflake phone screen",
    "snowflake hackerrank",
    "snowflake codesignal",
    "snowflake new grad",
    "snowflake intern",
    "snowflake system design",
    "snowflake offer",
    "snowflake rejected",
    "snowflake ic1",
    "snowflake ic2",
    "snowflake backend interview",
    "snowflake chakra",
    "snowflake ai interview",
]
HN_QUERIES = [
    "snowflake interview",
    "snowflake onsite",
    "snowflake hiring engineer",
    "snowflake interview process",
]

RELEVANT_RE = re.compile(r"snowflake", re.I)
CTX_RE = re.compile(r"interview|\boa\b|onsite|screen|offer|assessment|hackerrank|codesignal|chakra", re.I)


def log(msg: str) -> None:
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def main() -> None:
    stamp = time.strftime("%Y-%m-%d")
    all_hits_by_sub: dict[str, list[dict]] = {}

    # 1. Reddit search matrix
    for sub in SUBS:
        seen: dict[str, dict] = {}
        for q in QUERIES:
            try:
                hits = harvest.reddit_search(sub, q)
            except Exception as exc:  # noqa: BLE001
                log(f"! reddit r/{sub} {q!r}: {exc}")
                hits = []
            new = 0
            for h in hits:
                if h["id"] and h["id"] not in seen:
                    seen[h["id"]] = h
                    new += 1
            log(f"reddit r/{sub} {q!r} -> {len(hits)} (new {new}, total {len(seen)})")
            time.sleep(3.5)
        path = HARVEST_DIR / f"reddit_{sub}_{stamp}.json"
        rows = sorted(seen.values(), key=lambda h: h.get("published", ""), reverse=True)
        path.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
        all_hits_by_sub[sub] = rows
        log(f"== r/{sub} done: {len(rows)} unique posts -> {path.name}")

    # 2. Filter candidates for full-text fetch: title mentions snowflake AND interview-ish context
    candidates = []
    for sub, rows in all_hits_by_sub.items():
        for h in rows:
            title = h.get("title", "")
            if RELEVANT_RE.search(title) and CTX_RE.search(title):
                candidates.append(h)
    # most recent first (published desc), cap 60
    candidates.sort(key=lambda h: h.get("published", ""), reverse=True)
    candidates = candidates[:60]
    log(f"candidates for full-text fetch (title matches): {len(candidates)}")

    posts = []
    posts_path = HARVEST_DIR / f"reddit_posts_{stamp}.json"
    for i, h in enumerate(candidates, 1):
        try:
            p = harvest.reddit_post(h["sub"], h["id"])
        except Exception as exc:  # noqa: BLE001
            log(f"! reddit-post {h['id']}: {exc}")
            continue
        p["published"] = h.get("published", "")
        p["query"] = h.get("query", "")
        posts.append(p)
        if i % 5 == 0 or i == len(candidates):
            posts_path.write_text(json.dumps(posts, ensure_ascii=False, indent=1), encoding="utf-8")
            log(f"  reddit-post {i}/{len(candidates)} saved ({len(posts)} ok)")
        time.sleep(3.5)
    posts_path.write_text(json.dumps(posts, ensure_ascii=False, indent=1), encoding="utf-8")
    log(f"== reddit-post done: {len(posts)} full posts -> {posts_path.name}")

    # 3. Also do body-mentions-snowflake sweep for posts whose title didn't match but body might
    # (cheap extra pass over remaining unique posts not already fetched, capped)
    fetched_ids = {p["id"] for p in posts}
    remaining = []
    for sub, rows in all_hits_by_sub.items():
        for h in rows:
            if h["id"] not in fetched_ids and RELEVANT_RE.search(h.get("title", "")):
                remaining.append(h)
    remaining.sort(key=lambda h: h.get("published", ""), reverse=True)
    remaining = remaining[: max(0, 60 - len(posts))]
    log(f"extra snowflake-title-only candidates to spot check: {len(remaining)}")
    extra_posts = []
    extra_path = HARVEST_DIR / f"reddit_posts_extra_{stamp}.json"
    for i, h in enumerate(remaining, 1):
        try:
            p = harvest.reddit_post(h["sub"], h["id"])
        except Exception as exc:  # noqa: BLE001
            log(f"! reddit-post(extra) {h['id']}: {exc}")
            continue
        p["published"] = h.get("published", "")
        p["query"] = h.get("query", "")
        extra_posts.append(p)
        if i % 5 == 0 or i == len(remaining):
            extra_path.write_text(json.dumps(extra_posts, ensure_ascii=False, indent=1), encoding="utf-8")
            log(f"  reddit-post(extra) {i}/{len(remaining)} saved")
        time.sleep(3.5)
    if remaining:
        extra_path.write_text(json.dumps(extra_posts, ensure_ascii=False, indent=1), encoding="utf-8")
        log(f"== extra reddit-post done: {len(extra_posts)} -> {extra_path.name}")

    # 4. Hacker News
    hn_rows = []
    seen_hn = set()
    for q in HN_QUERIES:
        for tags in ("comment", "story"):
            try:
                rows = harvest.hn_search(q, tags=tags)
            except Exception as exc:  # noqa: BLE001
                log(f"! hn {q!r} {tags}: {exc}")
                rows = []
            new = 0
            for r in rows:
                if r["id"] not in seen_hn:
                    seen_hn.add(r["id"])
                    hn_rows.append(r)
                    new += 1
            log(f"hn {q!r} ({tags}) -> {len(rows)} (new {new}, total {len(hn_rows)})")
            time.sleep(1.0)
    hn_path = HARVEST_DIR / f"hn_{stamp}.json"
    hn_path.write_text(json.dumps(hn_rows, ensure_ascii=False, indent=1), encoding="utf-8")
    log(f"== hn done: {len(hn_rows)} rows -> {hn_path.name}")

    log("ALL DONE")


if __name__ == "__main__":
    main()
