"""The LeetCode knowledge tree: 灵茶山艾府 (0x3F)'s problem lists, as deep as his posts go, with our problems hung on it.

    uv run python scripts/lc_tree.py            # writes sources/local/lc/tree.json and prints the tree with counts
    uv run python scripts/lc_tree.py --thin     # also lists the leaves holding one problem of ours, with candidates
    uv run python scripts/lc_tree.py --write    # also writes the domain leetcode-tree: its skeleton and a stub card per
                                                # problem (learning cards, lct-learn-*, are written by hand or by agents)

The posts are kept in sources/local/lc/0x3f/posts/<list>.md (local only: his text). Levels follow the headings:
list -> 一、二、… -> §1.1 -> §2.1.1, in his order; the lists in the order he recommends studying them. A leaf is a heading
with problems under it. Each leaf keeps its problems from his post (`candidates`: slug, number, title, rating, members
only) and the articles he links for its technique (`articles`). Our problems hang on their leaf: a problem listed in
several leaves goes to the one in the list of its main technique, else to the first. Problems in no list are not dealt.

Order (Chi, 2026-11-11: by asked-frequency, coverage and importance, 80/20; the lists in any order, the headings inside a
list in his order). A node's weight is the importance (public company-wise frequency) summed over its problems. Lists
go heaviest first; inside a list the headings keep his order; inside a leaf, problems go most asked first. `core`
is the smallest set of problems that carries `CORE_SHARE` of all importance: the daily deck deals those first.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LC = ROOT / "sources/local/lc"
HOME = LC / "0x3f"
POSTS = HOME / "posts"
ORDER = ["sliding-window", "binary-search", "monotonic-stack", "grid", "bits", "graph", "dp", "data-structures", "math",
         "greedy", "list-tree-backtracking", "string"]  # the order 0x3F recommends
PATTERN_LIST = {"01-hashing": "data-structures", "02-prefix-sum": "data-structures", "03-two-pointers": "sliding-window",
                "04-sliding-window": "sliding-window", "05-monotonic-stack": "monotonic-stack", "06-binary-search": "binary-search",
                "07-heap": "data-structures", "08-intervals": "greedy", "09-linked-list": "list-tree-backtracking",
                "10-tree-dfs": "list-tree-backtracking", "11-tree-bfs-bst": "list-tree-backtracking", "12-graph": "graph",
                "13-topo-sort": "graph", "14-union-find": "data-structures", "15-shortest-path": "graph",
                "16-backtracking": "list-tree-backtracking", "17-dp": "dp", "18-greedy": "greedy", "19-trie": "data-structures",
                "20-design": "data-structures", "21-string": "string", "22-math-bit": "math"}
CORE_SHARE = 0.8  # the problems carrying this share of all importance are dealt first
SECTION = re.compile(r"^(#{2,5}) (?:([零一二三四五六七八九十]+)、|§([\d.]+) )(.+)$")
NUMERAL = "零一二三四五六七八九十"
PROBLEM = re.compile(r"^\s*- \[(\d+)\. ([^\]]+)\]\(https://leetcode\.cn/problems/([a-z0-9-]+)/?\)(.*)$")
ARTICLE = re.compile(r"\[([^\]]+)\]\((https://leetcode\.cn/(?:problems/[a-z0-9-]+/solutions|circle/discuss|discuss/post)/[^)\s]+)\)")


def chinese(n: str) -> int:
    """零 … 九十九."""
    if "十" not in n:
        return NUMERAL.index(n)
    tens, _, ones = n.partition("十")
    return (NUMERAL.index(tens) if tens else 1) * 10 + (NUMERAL.index(ones) if ones else 0)


def parse(name: str) -> dict:
    """One post as a tree: {title, children: [...]} with problems on the leaves."""
    text = (POSTS / f"{name}.md").read_text(encoding="utf-8")
    title = text.splitlines()[0].lstrip("# ")
    m = re.search(r"】(.+?)（", title)
    root = {"title": m.group(1) if m else title, "key": name, "id": name, "children": [], "articles": []}
    stack, fenced = [(1, root)], False
    for line in text.splitlines():
        if line.startswith("```"):
            fenced = not fenced
            continue
        if fenced:  # code: a `#` line there is a comment, not a heading
            if not root.get("closed") and len(stack) > 1:
                stack[-1][1]["text"] = stack[-1][1].get("text", "") + line + "\n"
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
            num = str(chinese(s.group(2))) if s.group(2) else s.group(3).split(".")[-1]  # 十二、 -> 12, §2.1.1 -> 1
            while stack[-1][0] >= level:
                stack.pop()
            # the parent's id plus this heading's own number: sliding-window.2.1.1 for §2.1.1 under §2.1 under 二、
            node = {"title": s.group(4).strip(), "id": f"{stack[-1][1]['id']}.{num}", "children": [], "articles": [], "candidates": []}
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
            if line.strip():
                node["text"] = node.get("text", "") + line + "\n"
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
    exp = json.loads((LC / "expand.json").read_text(encoding="utf-8")) if (LC / "expand.json").exists() else {}
    body = ROOT / "vault/interviews/core/leetcode/problems"
    for lst in lists:
        for path, leaf in leaves(lst):
            ours = home.get((lst["key"], path), [])
            # problems added to a thin leaf (expand.json) join after ours once their answer body exists
            leaf["problems"] = ours + [c["slug"] for c in exp.get(leaf["id"], []) if c["slug"] not in ours and (body / f"{c['slug']}.md").exists()]
    weight = {slug: p["importance"] for slug, p in probs.items()}
    weight.update({c["slug"]: c.get("importance", 0.0) for v in exp.values() for c in v})
    lists = prioritize(lists, weight)
    every = sorted({s for lst in lists for _, x in leaves(lst) for s in x["problems"]}, key=lambda s: -weight.get(s, 0.0))
    total, acc, core = sum(weight.get(s, 0.0) for s in every) or 1.0, 0.0, []
    for s in every:
        if acc >= CORE_SHARE * total:
            break
        core.append(s)
        acc += weight.get(s, 0.0)
    return {"lists": lists, "primary": primary, "core": core}


def prioritize(lists: list[dict], weight: dict[str, float]) -> list[dict]:
    """The lists heaviest first; inside a list his order is kept; inside a leaf, problems most asked first."""
    def mass(n: dict) -> float:
        n["weight"] = sum(weight.get(s, 0.0) for s in n.get("problems", [])) + sum(mass(c) for c in n["children"])
        return n["weight"]

    def order(n: dict) -> None:
        if n.get("problems"):
            n["problems"].sort(key=lambda s: -weight.get(s, 0.0))
        for c in n["children"]:
            order(c)
    for lst in lists:
        mass(lst)
        order(lst)
    return sorted(lists, key=lambda lst: -lst["weight"])


SKELETON = ROOT / "skeleton/leetcode-tree.yaml"  # local only, like the cards: built from 0x3F's posts
CARDS = ROOT / "vault/interviews/core/leetcode/tree/cards"
PROBLEMS = ROOT / "vault/interviews/core/leetcode/problems"


def card_id(leaf_id: str) -> str:
    return "lct-learn-" + leaf_id.replace(".", "-")


def write(t: dict) -> int:
    """The domain leetcode-tree: every leaf with a problem, its ancestors, a stub per problem (ours, then those added
    from expand.json), in the order the daily deck deals them."""
    import yaml

    def problems(leaf: dict) -> list[str]:
        return [s for s in leaf.get("problems", []) if (PROBLEMS / f"{s}.md").exists()]

    def node(n: dict, path: tuple, top: str) -> dict | None:
        path = path + (n["title"],)
        kids = [k for c in n["children"] if (k := node(c, path, top))]
        mine = problems(n) if n.get("candidates") else []
        if not kids and not mine:
            return None  # no problem of ours here: left empty
        if mine:
            folder = CARDS / top / n["id"]
            folder.mkdir(parents=True, exist_ok=True)
            for step, slug in enumerate(mine, 2):  # step 1 is the leaf's learning card
                (folder / f"lct-{slug}.md").write_text(
                    f"---\nid: lct-{slug}\nnode: {n['id']}\ntype: qa\nstep: {step}\nbody: interviews/core/leetcode/problems/{slug}\n"
                    f"meta: \"灵神题单 · {' › '.join(path)}\"\n---\n", encoding="utf-8")
        out = {"id": n["id"], "title": n["title"], "summary": " › ".join(path)}
        if kids:
            out["children"] = kids
        return out

    nodes = []
    for i, lst in enumerate(t["lists"], 1):
        n = node(lst, (), lst["key"])
        if n:
            nodes.append({**n, "order": i})
    SKELETON.write_text("# Generated by scripts/lc_tree.py --write from 0x3F's problem-list posts. Local only.\n" + yaml.safe_dump(
        {"domain": "leetcode-tree", "title": "算法知识树（灵神题单）", "lang": "zh", "vault": "interviews/core/leetcode/tree",
         "examples_from": "interviews/core/leetcode/problems", "fold": "bullets", "nodes": nodes},
        allow_unicode=True, sort_keys=False), encoding="utf-8")
    return sum(1 for _ in CARDS.rglob("lct-*.md"))


def material(t: dict, leaf_id: str) -> str:
    """What a learning card for one leaf is written from: the post's words on the leaf and its ancestors, the articles
    it links that are on disk, and his solutions of the leaf's problems that are on disk."""
    out = []
    for lst in t["lists"]:
        for path, leaf in leaves(lst):
            if leaf["id"] != leaf_id:
                continue
            chain, n = [], lst
            for title in path[1:]:
                n = next(c for c in n["children"] if c["title"] == title)
                chain.append(n)
            out.append(f"# {' › '.join(path)}  ({leaf_id})\n")
            for n in [lst] + chain:
                if n.get("text"):
                    out.append(f"## 帖中文字 · {n['title']}\n{n['text']}")
            arts = [a for n in [lst] + chain for a in n.get("articles", [])]
            for a in arts:
                f = HOME / "articles" / f"{a['url'].rstrip('/').split('/')[-1]}.md"
                if f.exists():
                    out.append(f"## 链接文章（已下载）: {f.relative_to(ROOT)}  — {a['title']}")
            ours = leaf.get("problems", [])
            out.append("## 我们在这一节的题: " + ", ".join(ours))
            out.append("## 这一节的全部题（灵神顺序）: " + "; ".join(f"{c['num']} {c['title']}" + (f" ({c['rating']})" if c["rating"] else "")
                                                       for c in leaf["candidates"]))
            for slug in dict.fromkeys(ours + [c["slug"] for c in leaf["candidates"][:2]]):
                f = HOME / "solutions" / f"{slug}.md"
                if f.exists():
                    out.append(f"## 灵神题解（已下载）: {f.relative_to(ROOT)}")
            return "\n".join(out)
    raise SystemExit(f"no leaf {leaf_id}")


def main() -> int:
    if "--leaf" in sys.argv:
        print(material(build(), sys.argv[sys.argv.index("--leaf") + 1]))
        return 0
    t = build()
    (LC / "tree.json").write_text(json.dumps(t, ensure_ascii=False, indent=1), encoding="utf-8")
    thin = []
    for lst in t["lists"]:
        ls = leaves(lst)
        ours = sum(len(leaf["problems"]) for _, leaf in ls)
        print(f"{lst['title']}: {len(ls)} leaves, {sum(1 for _, x in ls if x['problems'])} with ours, {ours} problems")
        thin += [(p, x) for p, x in ls if len(x["problems"]) == 1]
    print(f"{len(t['primary'])} problems placed · {len(thin)} leaves hold one problem of ours")
    if "--write" in sys.argv:
        print(f"{write(t)} cards under {CARDS.relative_to(ROOT)} · skeleton {SKELETON.relative_to(ROOT)}")
    if "--thin" in sys.argv:
        for path, leaf in thin:
            print("  " + " › ".join(path), "|", leaf["problems"][0])
    return 0


if __name__ == "__main__":
    sys.exit(main())
