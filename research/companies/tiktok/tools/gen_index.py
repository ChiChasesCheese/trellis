"""Write vault/interviews/core/leetcode/tiktok/README.md: the problem list in study order, each row linking its
whole-answer card. Only problems whose whole card exists are listed (re-run after every card group).

    uv run python research/companies/tiktok/tools/gen_index.py
"""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[4]
DECK = ROOT / "vault/interviews/core/leetcode/tiktok"
sk = yaml.safe_load((ROOT / "skeleton/tiktok-lc.yaml").read_text(encoding="utf-8"))
index = __import__("json").loads((ROOT / "research/companies/tiktok/index.json").read_text(encoding="utf-8"))

TAG_ZH = {"Array": "数组", "Hash Table": "哈希", "String": "字符串", "Dynamic Programming": "动态规划",
          "Sliding Window": "滑动窗口", "Two Pointers": "双指针", "Binary Search": "二分", "Stack": "栈",
          "Monotonic Stack": "单调栈", "Heap (Priority Queue)": "堆", "Linked List": "链表", "Tree": "树",
          "Depth-First Search": "DFS", "Breadth-First Search": "BFS", "Graph Theory": "图", "Union-Find": "并查集",
          "Topological Sort": "拓扑排序", "Backtracking": "回溯", "Greedy": "贪心", "Design": "设计",
          "Trie": "字典树", "Prefix Sum": "前缀和", "Sorting": "排序", "Math": "数学", "Matrix": "矩阵",
          "Bit Manipulation": "位运算", "Simulation": "模拟", "Divide and Conquer": "分治", "Recursion": "递归"}

lines = ["# TikTok 字节高频题：总表", "",
         "TikTok 和字节（美国与国内）面试里最常出现的编程题，按学习顺序排列：A 档最高频，B 档次之，档内按热度降序。"
         "点开每一行就是该题的完整标准答案（识别信号、推导、代码、复杂度、易错点、追问）。Anki 里同样的内容在"
         " `LeetCode Tops::24 TikTok 字节高频 · 整题答案`，拆成小卡的版本在 `::25 … · 拆分背诵`。"
         "先刷模式识别 [[interviews/core/leetcode/tiktok/map/patterns|patterns]] 和 Python 工具箱 [[interviews/core/leetcode/tiktok/map/python|python]]。", ""]
count = 0
for branch in sk["nodes"]:
    if branch["id"] not in ("a", "b", "p1", "p2", "p3", "p4", "p5"):
        continue
    rows = []
    for leaf in branch["children"]:
        slug = leaf["id"].split(".", 1)[1]
        if not (DECK / "cards" / branch["id"] / f"tlc-{slug}-0-whole.md").exists():
            continue
        p = index.get(slug, {})
        tags = "、".join(dict.fromkeys(TAG_ZH[t] for t in p.get("tags", []) if t in TAG_ZH)) or "—"
        rows.append(f"| [[tlc-{slug}-0-whole\\|{leaf['title']}]] | {p.get('difficulty') or '—'} | {tags} |")
    if rows:
        lines += [f"## {branch['title']}", "", "| 题 | 难度 | 主要考点 |", "|---|---|---|", *rows, ""]
        count += len(rows)
(DECK / "README.md").write_text("\n".join(lines), encoding="utf-8")
print(count, "problems listed")
