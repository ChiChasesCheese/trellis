"""Daily LeetCode deck: pick up the problems Chi solved recently and queue them for cards.

    uv run python scripts/leetcode_daily.py fetch      # new accepted problems -> skeleton leaves + statements
    uv run python scripts/leetcode_daily.py pending    # leaves that still have no card

LeetCode's public GraphQL (`recentAcSubmissionList`) lists a user's last 20 accepted submissions without logging in;
the submitted code itself needs a login, so cards carry a best-practice solution, not Chi's own code. The username and
the set of problems already taken live in `sources/local/leetcode-daily/state.json` (gitignored: the repo is public).
A problem that already has a whole-answer card in another LeetCode deck is recorded but gets no second card.
Leaves go under one branch per month in `skeleton/leetcode-daily.yaml`; cards are written by the daily session that
follows `research/leetcode-daily/AGENT.md`.
"""
from __future__ import annotations

import html
import json
import re
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
LOCAL = ROOT / "sources/local/leetcode-daily"
STATE = LOCAL / "state.json"
SKELETON = ROOT / "skeleton/leetcode-daily.yaml"
CARDS = ROOT / "vault/interviews/core/leetcode/daily/cards"
OTHER_CARDS = [ROOT / "vault/interviews/core/leetcode/tiktok/cards"]
IN_DECKS = ROOT / "sources/local/lc-in-decks.json"
HEADER = ("# LeetCode problems Chi solved, one whole-answer card each, one branch per month.\n"
          "# Leaves are appended by scripts/leetcode_daily.py fetch; cards follow research/leetcode-daily/AGENT.md.\n")


def gql(host: str, query: str, variables: dict) -> dict:
    path = "/graphql/" if host.endswith(".cn") else "/graphql"
    req = urllib.request.Request(f"https://{host}{path}", data=json.dumps({"query": query, "variables": variables}).encode(),
                                 headers={"Content-Type": "application/json", "Referer": f"https://{host}",
                                          "User-Agent": "curl/8.7.1"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read())["data"]
        except OSError:
            if attempt == 4:
                raise
            time.sleep(2 ** attempt)
    return {}


def recent(username: str) -> list[dict]:
    q = "query($u:String!,$n:Int!){recentAcSubmissionList(username:$u,limit:$n){titleSlug timestamp lang}}"
    return gql("leetcode.com", q, {"u": username, "n": 20})["recentAcSubmissionList"] or []


def question(slug: str) -> dict:
    q = ("query($s:String!){question(titleSlug:$s){questionFrontendId title translatedTitle difficulty content "
         "translatedContent topicTags{name}}}")
    cn = gql("leetcode.cn", q, {"s": slug}).get("question") or {}
    if cn.get("translatedContent") or cn.get("content"):
        return cn
    return gql("leetcode.com", q.replace(" translatedTitle", "").replace(" translatedContent", ""), {"s": slug}).get("question") or cn


def to_text(raw: str) -> str:
    text = re.sub(r"<sup>\s*(.*?)\s*</sup>", r"^\1", raw or "")
    text = re.sub(r"<(pre|p|div|li|ul|ol|br)[^>]*>", "\n", text)
    text = re.sub(r"</?[a-zA-Z][^>]*>", "", text)
    return re.sub(r"\n{3,}", "\n\n", html.unescape(text)).strip()


def existing_card(slug: str, pid: str) -> str:
    for folder in OTHER_CARDS:
        for f in folder.glob(f"*/tlc-{slug}-0-whole.md"):
            return str(f.relative_to(ROOT))
    if IN_DECKS.exists() and pid.isdigit():
        hits = json.loads(IN_DECKS.read_text(encoding="utf-8")).get(pid) or []
        if hits:
            return hits[0].get("source") or hits[0].get("deck", "")
    return ""


def load_skeleton() -> dict:
    if SKELETON.exists():
        return yaml.safe_load(SKELETON.read_text(encoding="utf-8"))
    return {"domain": "leetcode-daily", "title": "LeetCode 每日刷题", "deck": "LeetCode Tops::28 Daily（每日刷题）",
            "lang": "zh", "vault": "interviews/core/leetcode/daily",
            "examples_from": "interviews/core/leetcode/tiktok/cards,interviews/core/leetcode/daily/cards",
            "study": {"order": "core-first", "mix": "new-first", "new_per_day": 10, "reviews_per_day": 200},
            "nodes": []}


def fetch() -> int:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    seen = state.setdefault("seen", {})
    sk = load_skeleton()
    added = 0
    for sub in sorted(recent(state["username"]), key=lambda s: int(s["timestamp"])):
        slug = sub["titleSlug"]
        if slug in seen:
            continue
        q = question(slug)
        if not q:
            print(f"skip {slug}: no question data")
            continue
        day = datetime.fromtimestamp(int(sub["timestamp"])).strftime("%Y-%m-%d")
        pid = str(q.get("questionFrontendId") or "")
        title_zh = q.get("translatedTitle") or q["title"]
        other = existing_card(slug, pid)
        seen[slug] = {"id": pid, "title": q["title"], "title_zh": title_zh, "difficulty": q.get("difficulty", ""),
                      "tags": [t["name"] for t in q.get("topicTags") or []], "solved": day, "covered_by": other}
        if other:
            print(f"covered {slug} ({day}): {other}")
            continue
        LOCAL.mkdir(parents=True, exist_ok=True)
        (LOCAL / f"{slug}.txt").write_text(to_text(q.get("translatedContent") or q.get("content") or ""), encoding="utf-8")
        month = day[:7]
        branch = next((n for n in sk["nodes"] if n["id"] == month), None)
        if branch is None:
            branch = {"id": month, "order": 0, "title": f"{month} 解出的题", "summary": f"{month} 在 LeetCode 上解出的题，按解出时间排。",
                      "children": []}
            sk["nodes"].append(branch)
        name = f"LC {pid} {title_zh}" + (f"（{q['title']}）" if title_zh != q["title"] else "")
        branch["children"].append({"id": f"{month}.{slug}", "title": name,
                                   "summary": f"{q.get('difficulty', '')}；{day} 解出；{', '.join(seen[slug]['tags'][:4])}。"})
        print(f"new {month}.{slug} ({day})")
        added += 1
        time.sleep(0.4)
    sk["nodes"].sort(key=lambda n: n["id"], reverse=True)  # newest month first
    for i, n in enumerate(sk["nodes"], 1):
        n["order"] = i
        n["core"] = True
    SKELETON.write_text(HEADER + yaml.safe_dump(sk, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{added} new leaf/leaves")
    return 0


def pending() -> int:
    sk = load_skeleton()
    todo = [leaf["id"] for n in sk["nodes"] for leaf in n["children"]
            if not (CARDS / n["id"] / f"tlc-daily-{leaf['id'].split('.', 1)[1]}-0-whole.md").exists()]
    print("\n".join(todo) or "nothing pending")
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "fetch"
    sys.exit({"fetch": fetch, "pending": pending}[cmd]())
