"""The LeetCode knowledge tree: 灵茶山艾府 (0x3F)'s problem lists, as deep as his posts go, with our problems hung on it.

    uv run python scripts/lc_tree.py            # writes sources/local/lc/tree.json and prints the tree with counts
    uv run python scripts/lc_tree.py --thin     # also lists the leaves holding one problem of ours, with candidates

The posts are kept in sources/local/lc/0x3f/posts/<list>.md (local only: his text). Levels follow the headings:
list -> 一、二、… -> §1.1 -> §2.1.1, in his order; the lists in the order he recommends studying them. A leaf is a heading
with problems under it. Each leaf keeps its problems from his post (`candidates`: slug, number, title, rating, members
only) and the articles he links for its technique (`articles`). Our problems hang on their leaf: a problem listed in
several leaves goes to the one in the list of its main technique, else to the first. Problems in no list are not dealt.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LC = ROOT / "sources/local/lc"
POSTS = LC / "0x3f/posts"
ORDER = ["sliding-window", "binary-search", "monotonic-stack", "grid", "bits", "graph", "dp", "data-structures", "math",
         "greedy", "list-tree-backtracking", "string"]  # the order 0x3F recommends
PATTERN_LIST = {"01-hashing": "data-structures", "02-prefix-sum": "data-structures", "03-two-pointers": "sliding-window",
                "04-sliding-window": "sliding-window", "05-monotonic-stack": "monotonic-stack", "06-binary-search": "binary-search",
                "07-heap": "data-structures", "08-intervals": "greedy", "09-linked-list": "list-tree-backtracking",
                "10-tree-dfs": "list-tree-backtracking", "11-tree-bfs-bst": "list-tree-backtracking", "12-graph": "graph",
                "13-topo-sort": "graph", "14-union-find": "data-structures", "15-shortest-path": "graph",
                "16-backtracking": "list-tree-backtracking", "17-dp": "dp", "18-greedy": "greedy", "19-trie": "data-structures",
                "20-design": "data-structures", "21-string": "string", "22-math-bit": "math"}
SECTION = re.compile(r"^(#{2,5}) (?:([零一二三四五六七八九十]+)、|§[\d.]+ )(.+)$")
PROBLEM = re.compile(r"^\s*- \[(\d+)\. ([^\]]+)\]\(https://leetcode\.cn/problems/([a-z0-9-]+)/?\)(.*)$")
ARTICLE = re.compile(r"\[([^\]]+)\]\((https://leetcode\.cn/(?:problems/[a-z0-9-]+/solutions|circle/discuss|discuss/post)/[^)\s]+)\)")


def parse(name: str) -> dict:
    """One post as a tree: {title, children: [...]} with problems on the leaves."""
    text = (POSTS / f"{name}.md").read_text(encoding="utf-8")
    title = text.splitlines()[0].lstrip("# ")
    m = re.search(r"】(.+?)（", title)
    root = {"title": m.group(1) if m else title, "key": name, "children": [], "articles": []}
    stack, fenced = [(1, root)], False
    for line in text.splitlines():
        if line.startswith("```"):
            fenced = not fenced
            continue
        if fenced:  # code: a `#` line there is a comment, not a heading
            continue
        if line.startswith("#"):
            s = SECTION.match(line)
            if not s:
                if line.startswith("## ") and root["children"]:  # 思考, 关联题单 … after the sections: they are over
                    stack = [(1, root)]
                    root["closed"] = True
                continue
            if root.get("closed"):
                continue
            level = len(s.group(1))
            node = {"title": s.group(3).strip(), "children": [], "articles": [], "candidates": []}
            while stack[-1][0] >= level:
                stack.pop()
            stack[-1][1]["children"].append(node)
            stack.append((level, node))
            continue
        if root.get("closed"):
            continue
        node = stack[-1][1]
        p = PROBLEM.match(line)
        if p:
            rest = p.group(4)
            r = re.match(r"\s*(\d{3,4})", rest)
            node.setdefault("candidates", []).append({"num": int(p.group(1)), "title": p.group(2), "slug": p.group(3),
                                                      "rating": int(r.group(1)) if r else None, "members": "会员题" in rest})
        else:
            node["articles"] += [{"title": a, "url": u} for a, u in ARTICLE.findall(line)]
    return root


def leaves(node: dict, path: tuple = ()) -> list[tuple[tuple, dict]]:
    """Every heading with problems under it, in order, with its path of titles."""
    path = path + (node["title"],)
    out = [(path, node)] if node.get("candidates") else []
    for c in node["children"]:
        out += leaves(c, path)
    return out


def build() -> dict:
    analysis = json.loads((LC / "analysis.json").read_text(encoding="utf-8"))
    probs = analysis["problems"]
    tech = {t["id"]: t for t in json.loads((LC / "taxonomy.json").read_text(encoding="utf-8"))["techniques"]}
    lists = [parse(n) for n in ORDER if (POSTS / f"{n}.md").exists()]
    found: dict[str, list[tuple[str, tuple]]] = {}
    for lst in lists:
        for path, leaf in leaves(lst):
            for c in leaf["candidates"]:
                found.setdefault(c["slug"], []).append((lst["key"], path))

    def own_list(p: dict) -> str | None:
        t = tech.get(p["techniques"][0]) if p["techniques"] else None
        return PATTERN_LIST.get(t["pattern"] if t else (p["patterns"] or [""])[0])

    home: dict[tuple, list[str]] = {}
    primary = {}
    for p in sorted(probs.values(), key=lambda p: -p["importance"]):
        where = found.get(p["slug"])
        if not where:
            continue
        key, path = next((w for w in where if w[0] == own_list(p)), where[0])
        home.setdefault((key, path), []).append(p["slug"])
        primary[p["slug"]] = list(path)
    for lst in lists:
        for path, leaf in leaves(lst):
            leaf["problems"] = home.get((lst["key"], path), [])
    return {"lists": lists, "primary": primary}


def main() -> int:
    t = build()
    (LC / "tree.json").write_text(json.dumps(t, ensure_ascii=False, indent=1), encoding="utf-8")
    thin = []
    for lst in t["lists"]:
        ls = leaves(lst)
        ours = sum(len(leaf["problems"]) for _, leaf in ls)
        print(f"{lst['title']}: {len(ls)} leaves, {sum(1 for _, x in ls if x['problems'])} with ours, {ours} problems")
        thin += [(p, x) for p, x in ls if len(x["problems"]) == 1]
    print(f"{len(t['primary'])} problems placed · {len(thin)} leaves hold one problem of ours")
    if "--thin" in sys.argv:
        for path, leaf in thin:
            print("  " + " › ".join(path), "|", leaf["problems"][0])
    return 0


if __name__ == "__main__":
    sys.exit(main())
