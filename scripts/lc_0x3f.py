"""Material from 灵茶山艾府 (0x3F) on leetcode.cn, for the LeetCode knowledge tree. Everything lands in sources/local/lc/0x3f/
(local only: his text).

    uv run python scripts/lc_0x3f.py posts        # the problem-list posts -> posts/<list>.md
    uv run python scripts/lc_0x3f.py expand       # leaves holding one problem of ours: the most asked problems of the leaf
                                                  # we do not have -> sources/local/lc/expand.json
    uv run python scripts/lc_0x3f.py articles     # the technique articles the posts link -> articles/<slug>.md
    uv run python scripts/lc_0x3f.py solutions    # his solution of each leaf's first problems, ours and the expansion
                                                  # problems -> solutions/<problem>.md

Fetching skips what is already on disk; one request a second.
"""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
HOME = ROOT / "sources/local/lc/0x3f"
POSTS = {"0viNMK": "sliding-window", "SqopEo": "binary-search", "9oZFK9": "monotonic-stack", "YiXPXW": "grid", "dHn9Vk": "bits",
         "01LUak": "graph", "tXLS3i": "dp", "mOr1u6": "data-structures", "IYT3ss": "math", "g6KTKL": "greedy",
         "K0n2gO": "list-tree-backtracking", "SJFwQI": "string"}
AUTHOR = "endlesscheng"
EXPAND = 2  # problems added to a leaf that holds one of ours


def gql(query: str, variables: dict) -> dict:
    req = urllib.request.Request("https://leetcode.cn/graphql/", json.dumps({"query": query, "variables": variables}).encode(),
                                 {"Content-Type": "application/json", "Referer": "https://leetcode.cn/"})
    time.sleep(1)
    try:
        return json.load(urllib.request.urlopen(req, timeout=40))["data"] or {}
    except (urllib.error.URLError, TimeoutError, ValueError) as e:  # one bad slug must not stop the rest
        print(f"  request failed: {e}")
        return {}


def save(path: Path, title: str, url: str, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"# {title}\n\nsource: {url}\n\n" + content.replace("\r\n", "\n"), encoding="utf-8")


def posts() -> None:
    q = "query q($uuid: ID!) { qaQuestion(uuid: $uuid) { title content } }"
    for uuid, name in POSTS.items():
        d = gql(q, {"uuid": uuid})["qaQuestion"]
        save(HOME / "posts" / f"{name}.md", d["title"], f"https://leetcode.cn/circle/discuss/{uuid}/", d["content"])
        print(name, len(d["content"]))


def article(slug: str, url: str, out: Path) -> bool:
    if out.exists():
        return True
    d = gql('query a($slug: String!) { solutionArticle(slug: $slug) { title content } }', {"slug": slug}).get("solutionArticle")
    if not d:
        return False
    save(out, d["title"], url, d["content"])
    return True


def articles() -> None:
    import lc_tree
    tree = lc_tree.build()["lists"]
    urls = set()

    def walk(n):
        urls.update(a["url"] for a in n.get("articles", []))
        for c in n["children"]:
            walk(c)
    for lst in tree:
        walk(lst)
    for url in sorted(u for u in urls if "/solutions/" in u):
        slug = url.rstrip("/").split("/")[-1]
        print(("ok  " if article(slug, url, HOME / "articles" / f"{slug}.md") else "miss"), url)


def solution(problem: str) -> bool:
    """His solution of one problem, if he wrote one."""
    out = HOME / "solutions" / f"{problem}.md"
    if out.exists():
        return True
    q = ("query a($questionSlug: String!, $userInput: String) { questionSolutionArticles(questionSlug: $questionSlug, skip: 0, "
         "first: 10, orderBy: DEFAULT, userInput: $userInput, tagSlugs: []) { edges { node { slug author { username } } } } }")
    edges = (gql(q, {"questionSlug": problem, "userInput": AUTHOR}).get("questionSolutionArticles") or {}).get("edges", [])
    mine = [e["node"]["slug"] for e in edges if e["node"]["author"]["username"] == AUTHOR]
    return bool(mine) and article(mine[0], f"https://leetcode.cn/problems/{problem}/solutions/", out)


def expand() -> None:
    """For each leaf with exactly one problem of ours: its most asked problems we lack, by the same importance as ours."""
    import lc_analysis
    import lc_tree
    from lc_data import github_frequency
    freq = github_frequency()
    have = set(json.loads((ROOT / "sources/local/lc/analysis.json").read_text(encoding="utf-8"))["problems"])
    out = {}
    for lst in lc_tree.build()["lists"]:
        for path, leaf in lc_tree.leaves(lst):
            if len(leaf["problems"]) != 1:
                continue
            ranked = sorted(((lc_analysis.importance(freq[c["slug"]], lc_analysis.DEFAULT), c) for c in leaf["candidates"]
                             if c["slug"] not in have and c["slug"] in freq), key=lambda x: -x[0])
            picks = [c | {"importance": round(v, 4)} for v, c in ranked if v > 0][:EXPAND]
            if picks:
                out[leaf["id"]] = picks
    (ROOT / "sources/local/lc/expand.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{sum(len(v) for v in out.values())} problems for {len(out)} leaves")


def solutions() -> None:
    import lc_tree
    exp = json.loads((ROOT / "sources/local/lc/expand.json").read_text(encoding="utf-8")) if (ROOT / "sources/local/lc/expand.json").exists() else {}
    want = []
    for lst in lc_tree.build()["lists"]:
        for _, leaf in lc_tree.leaves(lst):
            if not leaf["problems"] and leaf["id"] not in exp:
                continue
            want += [c["slug"] for c in leaf["candidates"] if not c["members"]][:2] + leaf["problems"][:3] + [c["slug"] for c in exp.get(leaf["id"], [])]
    want = list(dict.fromkeys(want))
    got = sum(solution(s) for s in want)
    print(f"{got} of {len(want)} problems have his solution")


def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    fn = {"posts": posts, "expand": expand, "articles": articles, "solutions": solutions}.get(cmd)
    if not fn:
        print(__doc__)
        return 2
    fn()
    return 0


if __name__ == "__main__":
    sys.exit(main())
