"""Classic-lists deck: LeetCode Hot 100 ∪ Blind 75 ∪ LeetCode 75, one whole-answer card per problem, sub-decks by
knowledge point.

    uv run python research/classic-lists/build.py fetch      # lists + metadata -> index.json, statements -> sources/local/classic/
    uv run python research/classic-lists/build.py skeleton   # points.json + index.json -> skeleton/classic-lists.yaml

`points.json` maps each LC number to a knowledge point id (the TikTok deck's pattern branches plus a few extra);
cards follow research/classic-lists/AGENT.md.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))
from leetcode_daily import gql, question, to_text  # noqa: E402

LISTS = ("LeetCode Hot 100", "Blind 75", "LeetCode 75")
SHORT = {"LeetCode Hot 100": "Hot 100", "Blind 75": "Blind 75", "LeetCode 75": "LeetCode 75"}
# Knowledge points in learning order (prerequisites first); ids match the TikTok pattern branches where they exist
POINTS = [
    ("hashing", "哈希：查找、计数与分组"), ("two-pointers", "双指针"), ("sliding-window", "滑动窗口"),
    ("prefix-sum", "前缀和与差分"), ("stack", "栈与队列"), ("monotonic-stack", "单调栈与单调队列"),
    ("binary-search", "二分查找：在下标上与在答案上"), ("linked-list", "链表技巧"), ("tree-dfs", "二叉树 DFS：返回值与全局量"),
    ("tree-bfs-bst", "二叉树 BFS 与 BST 性质"), ("heap-patterns", "堆：Top-K、多路归并与双堆"), ("intervals-sweep", "区间与扫描线"),
    ("graph-traversal", "图与网格的 BFS / DFS"), ("topo-sort", "拓扑排序"), ("union-find", "并查集"),
    ("shortest-path", "最短路：Dijkstra 与其变体"), ("backtracking", "回溯"), ("trie", "字典树"), ("greedy", "贪心"),
    ("dp-linear", "动态规划：线性与状态机"), ("dp-grid-string", "动态规划：网格、双串与区间"), ("dp-knapsack", "动态规划：背包与计数"),
    ("design", "数据结构设计题"), ("string-parsing", "字符串处理与表达式解析"), ("matrix", "矩阵：原地变换与模拟"),
    ("math-bit-sim", "数学、位运算与模拟"),
]


def fetch() -> int:
    other = json.loads((ROOT / "research/companies/tiktok/catalog/other_lists.json").read_text(encoding="utf-8"))
    plan = gql("leetcode.com", "query($s:String!){studyPlanV2Detail(planSlug:$s){planSubGroups{name questions{"
               "questionFrontendId titleSlug}}}}", {"s": "leetcode-75"})["studyPlanV2Detail"]["planSubGroups"]
    members = {"LeetCode Hot 100": {int(x) for x in other["LeetCode Hot 100"]}, "Blind 75": {int(x) for x in other["Blind 75"]},
               "LeetCode 75": {int(q["questionFrontendId"]) for g in plan for q in g["questions"]}}
    group75 = {int(q["questionFrontendId"]): g["name"] for g in plan for q in g["questions"]}
    meta = json.loads((ROOT / "research/companies/tiktok/catalog/lc_meta.json").read_text(encoding="utf-8"))
    slugs = {int(q["questionFrontendId"]): q["titleSlug"] for g in plan for q in g["questions"]}
    out_path = HERE / "index.json"
    index = json.loads(out_path.read_text(encoding="utf-8")) if out_path.exists() else {}
    for n in sorted(set().union(*members.values())):
        slug = slugs.get(n) or meta.get(str(n), {}).get("slug")
        if not slug:
            print(f"no slug for LC {n}")
            continue
        if str(n) in index and (ROOT / f"sources/local/classic/{slug}.txt").exists():
            continue
        q = question(slug)
        (ROOT / "sources/local/classic").mkdir(parents=True, exist_ok=True)
        (ROOT / f"sources/local/classic/{slug}.txt").write_text(
            to_text(q.get("translatedContent") or q.get("content") or ""), encoding="utf-8")
        index[str(n)] = {"id": n, "slug": slug, "title": q.get("title", ""), "title_zh": q.get("translatedTitle") or q.get("title", ""),
                         "difficulty": q.get("difficulty", ""), "tags": [t["name"] for t in q.get("topicTags") or []],
                         "lists": [SHORT[name] for name in LISTS if n in members[name]], "lc75_group": group75.get(n, "")}
        print(n, slug)
        time.sleep(0.4)
    out_path.write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(index), "problems")
    return 0


def skeleton() -> int:
    index = json.loads((HERE / "index.json").read_text(encoding="utf-8"))
    points = json.loads((HERE / "points.json").read_text(encoding="utf-8"))
    extra = points.pop("_new_points", {})
    titles = dict(POINTS) | extra
    order = [p for p, _ in POINTS] + sorted(extra)
    rank = {"Easy": 0, "Medium": 1, "Hard": 2}
    nodes = []
    for i, pid in enumerate([p for p in order if p in points.values()], 1):
        probs = sorted((index[n] for n, p in points.items() if p == pid),
                       key=lambda q: (rank.get(q["difficulty"], 1), -len(q["lists"]), q["id"]))
        nodes.append({"id": pid, "order": i, "core": True, "title": titles[pid],
                      "summary": f"{titles[pid]}：三个经典题单里属于这个知识点的题，先易后难。",
                      "children": [{"id": f"{pid}.{q['slug']}",
                                    "title": f"LC {q['id']} {q['title_zh']}" + (f"（{q['title']}）" if q['title_zh'] != q['title'] else ""),
                                    "summary": f"{q['difficulty']}；{'、'.join(q['lists'])}。"} for q in probs]})
    missing = sorted(set(index) - set(points), key=int)
    if missing:
        sys.exit(f"no knowledge point for: {missing}")
    sk = {"domain": "classic-lists", "title": "经典题单：Hot 100 ∪ Blind 75 ∪ LeetCode 75",
          "deck": "LeetCode Tops::29 经典题单（Hot 100 ∪ Blind 75 ∪ LeetCode 75）", "lang": "zh",
          "vault": "interviews/core/leetcode/classic",
          "examples_from": "interviews/core/leetcode/classic/cards,interviews/core/leetcode/tiktok/cards",
          "study": {"order": "core-first", "mix": "new-first", "new_per_day": 20, "reviews_per_day": 300}, "nodes": nodes}
    (ROOT / "skeleton/classic-lists.yaml").write_text(
        "# LeetCode Hot 100 ∪ Blind 75 ∪ LeetCode 75 by knowledge point. Generated by research/classic-lists/build.py.\n"
        + yaml.safe_dump(sk, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")
    print(sum(len(n["children"]) for n in nodes), "leaves in", len(nodes), "knowledge points")
    return 0


if __name__ == "__main__":
    sys.exit({"fetch": fetch, "skeleton": skeleton}[sys.argv[1]]())
