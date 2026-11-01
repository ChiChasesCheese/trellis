"""Daily LeetCode deck: pick up the problems Chi solved recently and queue them for cards.

    uv run python scripts/leetcode_daily.py fetch      # new accepted problems -> skeleton leaves + statements
    uv run python scripts/leetcode_daily.py pending    # leaves that still have no card

LeetCode's public GraphQL (`recentAcSubmissionList`) lists a user's last 20 accepted submissions without logging in;
the submitted code itself needs a login, so cards carry a best-practice solution, not Chi's own code. The username and
the set of problems already taken live in `sources/local/leetcode-daily/state.json` (gitignored: the repo is public).
A problem that already has a whole-answer card in another LeetCode deck is recorded but gets no second card.
Sub-decks are knowledge points (Chi, 2026-10-31), the same ones as the TikTok deck's pattern branches: `fetch` puts a
new leaf in `inbox`, and the session that writes its card moves it with `place <slug> <knowledge point>` (a new
knowledge point gets a title). Cards live flat in the cards folder, so a move only rewrites the `node:` line. The steps
are in `research/leetcode-daily/AGENT.md`.

    uv run python scripts/leetcode_daily.py place <slug> <point-id> ["中文标题"]   # move a leaf to a knowledge point
    uv run python scripts/leetcode_daily.py points                               # knowledge points in use / available
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
CARDS = ROOT / "vault/interviews/core/leetcode/daily/cards"  # flat: tlc-daily-<slug>-0-whole.md
OTHER_CARDS = [ROOT / "vault/interviews/core/leetcode/tiktok/cards"]
IN_DECKS = ROOT / "sources/local/lc-in-decks.json"
HEADER = ("# LeetCode problems Chi solved, one whole-answer card each, one branch per knowledge point.\n"
          "# Leaves are added by scripts/leetcode_daily.py fetch / place; cards follow research/leetcode-daily/AGENT.md.\n")
# The TikTok deck's pattern branches, in the same order (research/companies/tiktok/tools/gen_skeleton.py PATTERNS)
POINTS = [
    ("hashing", "哈希：查找、计数与分组"), ("prefix-sum", "前缀和与差分"), ("two-pointers", "双指针"),
    ("sliding-window", "滑动窗口"), ("monotonic-stack", "单调栈与单调队列"), ("binary-search", "二分查找：在下标上与在答案上"),
    ("heap-patterns", "堆：Top-K、多路归并与双堆"), ("intervals-sweep", "区间与扫描线"), ("linked-list", "链表技巧"),
    ("tree-dfs", "二叉树 DFS：返回值与全局量"), ("tree-bfs-bst", "二叉树 BFS 与 BST 性质"), ("graph-traversal", "图与网格的 BFS / DFS"),
    ("topo-sort", "拓扑排序"), ("union-find", "并查集"), ("shortest-path", "最短路：Dijkstra 与其变体"), ("backtracking", "回溯"),
    ("dp-linear", "动态规划：线性与状态机"), ("dp-grid-string", "动态规划：网格、双串与区间"), ("dp-knapsack", "动态规划：背包与计数"),
    ("greedy", "贪心"), ("trie", "字典树"), ("design", "数据结构设计题"), ("string-parsing", "字符串处理与表达式解析"),
    ("math-bit-sim", "数学、位运算与模拟"),
]
INBOX = ("inbox", "未归类（待放进知识点）")


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
    return {"domain": "leetcode-daily", "title": "LeetCode Daily：按知识点", "deck": "LeetCode Tops::28 Daily（按知识点）",
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
        branch = ensure_branch(sk, *INBOX)
        name = f"LC {pid} {title_zh}" + (f"（{q['title']}）" if title_zh != q["title"] else "")
        branch["children"].append({"id": f"inbox.{slug}", "title": name,
                                   "summary": f"{q.get('difficulty', '')}；{', '.join(seen[slug]['tags'][:4])}。"})
        print(f"new inbox.{slug}")
        added += 1
        time.sleep(0.4)
    save(sk)
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{added} new leaf/leaves")
    return 0


def ensure_branch(sk: dict, bid: str, title: str) -> dict:
    branch = next((n for n in sk["nodes"] if n["id"] == bid), None)
    if branch is None:
        branch = {"id": bid, "order": 0, "title": title, "summary": f"{title}：Chi 解过的题，按知识点归在一起。", "children": []}
        sk["nodes"].append(branch)
    return branch


def save(sk: dict) -> None:
    rank = {pid: i for i, (pid, _) in enumerate(POINTS)}
    sk["nodes"] = [n for n in sk["nodes"] if n["children"]]  # an emptied knowledge point leaves the deck
    sk["nodes"].sort(key=lambda n: (n["id"] == "inbox", rank.get(n["id"], len(POINTS)), n["id"]))
    for i, n in enumerate(sk["nodes"], 1):
        n["order"] = i
        n["core"] = True
    SKELETON.write_text(HEADER + yaml.safe_dump(sk, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")


def place(slug: str, point: str, title: str = "") -> int:
    sk = load_skeleton()
    title = title or dict(POINTS).get(point, "")
    if not title:
        sys.exit(f"{point} is a new knowledge point: give its Chinese title as the third argument")
    leaf = None
    for n in sk["nodes"]:
        for c in list(n["children"]):
            if c["id"].split(".", 1)[1] == slug:
                n["children"].remove(c)
                leaf = c
    if leaf is None:
        sys.exit(f"no leaf for {slug}")
    leaf["id"] = f"{point}.{slug}"
    ensure_branch(sk, point, title)["children"].append(leaf)
    save(sk)
    card = CARDS / f"tlc-daily-{slug}-0-whole.md"
    if card.exists():
        card.write_text(re.sub(r"^node: .*$", f"node: {leaf['id']}", card.read_text(encoding="utf-8"), count=1, flags=re.M),
                        encoding="utf-8")
    print(f"{slug} -> {leaf['id']}")
    return 0


def points() -> int:
    sk = load_skeleton()
    used = {n["id"]: len(n["children"]) for n in sk["nodes"]}
    for pid, title in POINTS + [(n["id"], n["title"]) for n in sk["nodes"] if n["id"] not in dict(POINTS)]:
        print(f"{pid:16} {used.get(pid, 0):3}  {title}")
    return 0


def pending() -> int:
    sk = load_skeleton()
    todo = [leaf["id"] for n in sk["nodes"] for leaf in n["children"]
            if n["id"] == "inbox" or not (CARDS / f"tlc-daily-{leaf['id'].split('.', 1)[1]}-0-whole.md").exists()]
    print("\n".join(todo) or "nothing pending")
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "fetch"
    args = sys.argv[2:]
    sys.exit({"fetch": fetch, "pending": pending, "place": place, "points": points}[cmd](*args))
