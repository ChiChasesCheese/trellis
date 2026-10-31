"""Write the LeetCode knowledge map: every problem in Chi's decks, organised by pattern, from basics to connections.

    uv run python research/companies/tiktok/tools/gen_knowledge_map.py

Universe: the TikTok deck (index.json), the Amazon and topic decks and the classic lists (catalog/other_lists.json).
A problem goes under every pattern its LeetCode topic tags (catalog/lc_meta.json) or the TikTok pattern cards name.
Inside a pattern, problems are ordered: TikTok P1..P4, then classic-list problems, then the rest. Output:
vault/interviews/core/leetcode/knowledge-map/ (README + one page per pattern). Re-run after the decks change.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
CAT = ROOT / "research/companies/tiktok/catalog"
OUT = ROOT / "vault/interviews/core/leetcode/knowledge-map"
index = json.loads((ROOT / "research/companies/tiktok/index.json").read_text(encoding="utf-8"))
lists = json.loads((CAT / "other_lists.json").read_text(encoding="utf-8"))
meta = {int(k): v for k, v in json.loads((CAT / "lc_meta.json").read_text(encoding="utf-8")).items()}
CLASSIC = ["Blind 75", "NeetCode 150", "LeetCode Hot 100", "Top Interview 150"]

# (id, title, LeetCode tags that put a problem here, one paragraph: what it is, what it grows from, what it connects to)
PATTERNS = [
 ("hashing", "哈希：查找、计数与分组", {"hash-table", "counting", "hash-function"},
  "起点。把「再扫一遍找」变成 O(1) 查表：补数查找、计数、按签名分组、去重。几乎所有后面的模式都会在内部用到哈希：前缀和要用哈希记出现过的前缀，滑动窗口要用哈希计窗口内的字符，图要用哈希存邻接表和访问标记。"),
 ("prefix-sum", "前缀和与差分", {"prefix-sum"},
  "从哈希长出来：区间和 = 两个前缀相减，「区间和等于 k」就变成「前面出现过某个前缀吗」，正是哈希查找。差分是它的逆运算，处理「很多区间批量加」。和滑动窗口的分界：数组有负数时窗口不单调，只能用前缀和加哈希。"),
 ("two-pointers", "双指针", {"two-pointers"},
  "利用有序或单调，把两层循环压成一次扫描：相向夹逼、快慢指针、原地分区。滑动窗口是同向双指针的特例；链表的找中点、判环也是快慢指针；归并排序的合并就是两个指针。"),
 ("sliding-window", "滑动窗口", {"sliding-window"},
  "同向双指针加一个可增量维护的窗口状态（哈希计数、和、单调队列）。前提是单调：窗口变大条件只会变坏或变好。不单调时退回前缀和；要窗口最大值时配单调队列。"),
 ("monotonic-stack", "单调栈与单调队列", {"monotonic-stack", "monotonic-queue"},
  "栈 / 队列里保持单调，每个元素进出一次：下一个更大元素、柱状图最大矩形、接雨水、滑动窗口最大值。是「找左右第一个比我大 / 小」这一类问题的通用骨架。"),
 ("binary-search", "二分查找", {"binary-search"},
  "从有序数组上的查找，推广到「答案单调」的判定：最小化最大值、能否在 x 内完成。旋转数组、找边界都是在维护一个不变量。和堆、平衡树一起，是「有序 + log n」的三件套。"),
 ("heap", "堆：Top-K、多路归并与调度", {"heap-priority-queue"},
  "只需要反复取最值时用堆：Top-K、K 路归并、双堆求中位数、按时间调度任务。Dijkstra 的本质就是「堆 + 贪心」；很多设计题（定时器、任务调度）的核心也是堆。"),
 ("intervals", "区间与扫描线", set(),
  "排序之后的线性扫描：合并、插入、求交、会议室数量。会议室问题可以用堆，也可以用差分 / 扫描线计数，两条路殊途同归。"),
 ("linked-list", "链表技巧", {"linked-list", "doubly-linked-list"},
  "指针操作的基本功：哑节点、快慢指针、原地反转、合并。LRU 的双向链表、K 个一组翻转都建立在这几个动作上。"),
 ("tree-dfs", "二叉树 DFS：递归的返回值", {"binary-tree", "tree"},
  "递归思维的主战场：后序返回子树信息（高度、路径和、是否平衡），前序向下传参数，全局量记录跨节点的答案。是回溯、树形 DP、图 DFS 的共同起点。"),
 ("tree-bfs-bst", "二叉树 BFS 与 BST", {"binary-search-tree"},
  "层序遍历（BFS 的最简形态）和 BST 的有序性：中序有序、上下界验证、第 k 小。BST 的有序性和二分查找是同一个思想。"),
 ("graph", "图与网格的 BFS / DFS", {"graph", "depth-first-search", "breadth-first-search", "matrix"},
  "把树的遍历推广到有环、有多个起点的结构：岛屿、连通分量、多源 BFS、最短步数。需要访问标记，这是和树遍历唯一的本质区别。"),
 ("topo-sort", "拓扑排序", {"topological-sort"},
  "有向无环图上的依赖顺序：课程表、构建顺序、外星字典。入度法就是 BFS，三色法就是 DFS 判环；DAG 上的最长路径还可以在拓扑序上做 DP。"),
 ("union-find", "并查集", {"union-find"},
  "动态维护「谁和谁连通」：连通分量、等价关系、账户合并。能做的事 BFS / DFS 也能做，但边是一条条加进来时并查集更自然。"),
 ("shortest-path", "最短路", {"shortest-path"},
  "无权图用 BFS；非负权用 Dijkstra（堆 + 贪心）；带状态（剩余次数、钥匙）就把状态并进节点。是图遍历和堆的合体。"),
 ("backtracking", "回溯", {"backtracking"},
  "枚举所有方案的 DFS：子集、组合、排列、分割、N 皇后。选择 / 递归 / 撤销三步，剪枝和去重决定快慢。加上记忆化就变成动态规划。"),
 ("dp", "动态规划", {"dynamic-programming", "memoization"},
  "回溯 + 记忆化 = 自顶向下 DP；反过来按顺序填表 = 自底向上 DP。线性 DP、网格 / 双串 DP、背包、区间 DP、树形 DP 都是「定义状态、写转移、定初值、定顺序」四步。"),
 ("greedy", "贪心", {"greedy"},
  "每一步做局部最优，并能用交换论证说明不会更差：跳跃游戏、分发糖果、区间调度。证明不出来时，往往要退回 DP。"),
 ("trie", "字典树", {"trie"},
  "把字符串的公共前缀合并成树：前缀查询、单词搜索 II、自动补全、按位异或最大值。是哈希做不到「按前缀查」时的答案。"),
 ("design", "数据结构设计", {"design", "data-stream", "iterator"},
  "把前面的结构拼成一个类：哈希 + 链表（LRU）、哈希 + 堆、哈希 + 数组（O(1) 随机）、时间版本的键值存储。考的是组合与不变量，不是新算法。"),
 ("string", "字符串处理与解析", {"string", "string-matching", "rolling-hash"},
  "字符串上的计数、匹配与解析：栈处理计算器和括号、递归下降解析嵌套结构、KMP 与滚动哈希做匹配。"),
 ("math-bit", "数学、位运算与模拟", {"math", "bit-manipulation", "simulation", "number-theory"},
  "取模与溢出、最大公约数、快速幂、异或去重、矩阵旋转与螺旋、按规则模拟。往往是一个「看出规律」的问题。"),
]
ORDER = [p[0] for p in PATTERNS]
pattern_cards = ROOT / "vault/interviews/core/leetcode/tiktok/cards/patterns"
card_names = {"hashing": "hashing", "prefix-sum": "prefix-sum", "two-pointers": "two-pointers", "sliding-window": "sliding-window",
              "monotonic-stack": "monotonic-stack", "binary-search": "binary-search", "heap": "heap-patterns",
              "intervals": "intervals-sweep", "linked-list": "linked-list", "tree-dfs": "tree-dfs", "tree-bfs-bst": "tree-bfs-bst",
              "graph": "graph-traversal", "topo-sort": "topo-sort", "union-find": "union-find", "shortest-path": "shortest-path",
              "backtracking": "backtracking", "dp": "dp-", "greedy": "greedy", "trie": "trie", "design": "design",
              "string": "string-parsing", "math-bit": "math-bit-sim"}

by_id = {p["id"]: (s, p) for s, p in index.items() if p.get("id")}
universe = set(by_id) | set(lists["Amazon"]) | set(lists["Topic decks"]) | {i for n in CLASSIC for i in lists[n]}
in_cards: dict[str, set[int]] = {}
for pid, name in card_names.items():
    nums: set[int] = set()
    for f in pattern_cards.glob(f"tlc-patterns-{name}*.md"):
        nums |= {int(n) for n in re.findall(r"LC\s*(\d+)", f.read_text(encoding="utf-8"))}
    in_cards[pid] = nums


def rank(i: int) -> tuple:
    if i in by_id:
        band = by_id[i][1].get("band", "b")
        if band != "b":
            return (0, band, -by_id[i][1].get("score", 0))
    if any(i in lists[n] for n in CLASSIC):
        return (1, "", i)
    return (2, "", i)


def line(i: int) -> str:
    m = meta.get(i, {})
    marks = []
    if i in by_id:
        s, p = by_id[i]
        marks.append("TikTok " + (p.get("band", "b").upper() if p.get("band") != "b" else "B"))
    if i in lists["Amazon"]:
        marks.append("Amazon")
    marks += [n for n in CLASSIC if i in lists[n]]
    d = {"EASY": "简单", "MEDIUM": "中等", "HARD": "困难"}.get(m.get("d", ""), "")
    title = f"LC {i} {m.get('zh') or (by_id[i][1].get('title_zh') if i in by_id else '')}"
    if i in by_id and list((ROOT / "vault/interviews/core/leetcode/tiktok/cards").glob(f"*/tlc-{by_id[i][0]}-0-whole.md")):
        title = f"[[tlc-{by_id[i][0]}-0-whole|{title}]]"
    return f"- {title}（{d}）· " + " · ".join(marks)


OUT.mkdir(parents=True, exist_ok=True)
counts = {}
for pid, title, tags, about in PATTERNS:
    members = sorted((i for i in universe
                      if (tags & set(meta.get(i, {}).get("tags", []))) or i in in_cards[pid]), key=rank)
    if pid == "tree-dfs":  # trees without a BST tag stay here; graph-style DFS lives under graph
        members = [i for i in members if {"tree", "binary-tree"} & set(meta.get(i, {}).get("tags", [])) or i in in_cards[pid]]
    core = [i for i in members if rank(i)[0] < 2]
    rest = [i for i in members if rank(i)[0] == 2]
    counts[pid] = (len(members), len(core))
    body = [f"# {title}", "", about, "",
            f"**先做（TikTok P1–P4 与经典题单，{len(core)} 道）**", "", *map(line, core), ""]
    if rest:
        body += [f"**再做（其余牌组里的题，{len(rest)} 道）**", "", *map(line, rest), ""]
    (OUT / f"{ORDER.index(pid) + 1:02d}-{pid}.md").write_text("\n".join(body), encoding="utf-8")

readme = ["# LeetCode 知识地图：由点到面", "",
          "把你所有牌组里的题（TikTok、Amazon、按专题分的牌组，以及 Blind 75、NeetCode 150、Hot 100、Top Interview 150）"
          "按解题模式排好。顺序就是学习顺序：前面的模式是后面的零件，越往后越是前面几样的组合。"
          "每一页先列 TikTok 高频和经典题单里的题，再列其余的题；能点开的题名直接跳到 TikTok 牌组的整题答案。", "",
          "| # | 模式 | 题数 | 先做 |", "|---|---|---|---|"]
for k, (pid, title, _, _) in enumerate(PATTERNS, 1):
    readme.append(f"| {k} | [[{k:02d}-{pid}|{title}]] | {counts[pid][0]} | {counts[pid][1]} |")
readme += ["", "**怎样由点到面**", "",
           "- **哈希**是零件：前缀和、滑动窗口、图、设计题都在内部用它。",
           "- **双指针 → 滑动窗口 → 单调队列**是一条线：同向扫描，再加上窗口状态，再加上窗口最值。",
           "- **前缀和**接在哈希后面，处理滑动窗口做不了的负数情况。",
           "- **树的 DFS → 回溯 → 动态规划**是一条线：递归返回值，枚举所有方案，再加记忆化。",
           "- **树的 BFS → 图的 BFS / DFS → 拓扑排序 / 最短路 / 并查集**是一条线：从无环到有环、从无权到有权。",
           "- **堆、二分、平衡树**是「有序 + log n」的三件套，Dijkstra 是堆加贪心。",
           "- **设计题**把以上结构拼成一个类，考的是组合与不变量。", ""]
(OUT / "README.md").write_text("\n".join(readme), encoding="utf-8")
print(len(universe), "problems;", {k: v[0] for k, v in counts.items()})
