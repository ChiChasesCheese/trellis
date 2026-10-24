"""Write skeleton/tiktok-lc.yaml from research/companies/tiktok/index.json (re-run overwrites it).

Branches: Python toolkit, pattern recognition, tier A, tier B. Problem leaves keep frequency order, so studying a
tier deck is studying by frequency, and patterns arrive mixed — the point of pattern-recognition practice.
"""
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[4]
index = json.loads((ROOT / "research/companies/tiktok/index.json").read_text(encoding="utf-8"))

PYTHON = [
 ("collections", "collections：Counter、defaultdict、deque、OrderedDict", "计数、分组、双端队列、有序字典在面试题里的地道用法，以及它们各自的复杂度和坑（Counter 相减丢负数、defaultdict 读也会插入、deque 随机访问是 O(n)）。"),
 ("heapq", "heapq：最小堆、Top-K、多路归并", "heapq 只有最小堆：最大堆取负、元组比较与平局、heapify 是 O(n)、nlargest/nsmallest、merge 多路归并、懒删除；什么时候堆不如排序或 quickselect。"),
 ("bisect-sorted", "bisect 与有序容器", "bisect_left/right 的语义与边界、key 参数、在有序列表上维护插入的代价；sortedcontainers.SortedList 在 LeetCode 可用时的 O(log n) 增删查。"),
 ("itertools-functools", "itertools 与 functools", "accumulate 做前缀和、pairwise、groupby 的前提、product/combinations/permutations、chain、islice；functools.cache 记忆化、reduce、cmp_to_key 自定义排序。"),
 ("idioms", "地道的 Python 写法", "解包与交换、enumerate/zip、推导式与生成器表达式、海象运算符、切片与反转、sorted 的 key 与稳定性、字符串 join、any/all、divmod、math.inf 与哨兵值。"),
 ("pitfalls", "Python 刷题的性能与正确性陷阱", "递归深度上限（sys.setrecursionlimit 与改迭代）、[[0]*n]*m 的别名、可变默认参数、list.pop(0)、字符串反复拼接、浮点比较、整数除法与负数取整、大输入下的常数。"),
 ("recursion-memo", "递归、记忆化与迭代改写", "@cache 记忆化搜索的写法与内存、cache_clear、把递归 DFS 改写成显式栈、nonlocal 与闭包、生成器递归。"),
 ("classes-design", "设计题的 Python 写法", "类设计题（LRU、迭代器、数据流）里的 __init__ 组织、dataclass、__slots__、__lt__ 让对象进堆、OrderedDict 实现 LRU、类型注解让代码更清楚。"),
]
PATTERNS = [
 ("signals", "从题面信号到模式：总览", "看到数据范围、输入形态、问法（最值 / 计数 / 存在性 / 构造）时分别该想到什么；n 的大小倒推复杂度。"),
 ("hashing", "哈希：查找、计数与分组", "补数查找、频次统计、签名分组、去重；什么时候用 set、dict、Counter；哈希的代价与有序需求。"),
 ("prefix-sum", "前缀和与差分", "前缀和 + 哈希求子数组和、前缀异或、二维前缀和、差分数组做区间加；为什么要先放入 {0: 1}。"),
 ("two-pointers", "双指针", "相向双指针（有序数组、夹逼）、同向快慢指针（去重、链表环）、分区；正确性来自哪个单调性。"),
 ("sliding-window", "滑动窗口", "可变窗口求最长 / 最短、固定窗口、「至多 k 个」减「至多 k-1 个」得「恰好 k 个」；窗口能用的前提是单调性。"),
 ("monotonic-stack", "单调栈与单调队列", "下一个更大 / 更小元素、柱状图最大矩形、接雨水、滑动窗口最大值；每个元素进出一次所以 O(n)。"),
 ("binary-search", "二分查找：在下标上与在答案上", "左闭右开模板、旋转数组、找边界；对答案二分（最小化最大值、能否在 x 内完成）的判断条件与单调性。"),
 ("heap-patterns", "堆：Top-K、多路归并与双堆", "Top-K 用大小为 k 的堆、K 路归并、双堆求中位数、按时间调度（会议室、任务）；懒删除。"),
 ("intervals-sweep", "区间与扫描线", "按左端点排序合并、按右端点排序的贪心选择、扫描线计数重叠、差分数组；端点相等时的处理。"),
 ("linked-list", "链表技巧", "哑节点、快慢指针找中点与环、原地反转、合并与拆分、深拷贝带随机指针；画图防止断链。"),
 ("tree-dfs", "二叉树 DFS：返回值与全局量", "后序返回子树信息（高度、路径和、是否平衡）、前序带参数下传、用全局最优记录跨节点路径；LCA 的三种情况。"),
 ("tree-bfs-bst", "二叉树 BFS 与 BST 性质", "层序遍历、按层统计、右视图；BST 中序有序、上下界验证、第 k 小、序列化与反序列化。"),
 ("graph-traversal", "图与网格的 BFS / DFS", "建图方式、网格四邻域、多源 BFS、最短步数用 BFS、连通分量计数、访问标记放在入队时。"),
 ("topo-sort", "拓扑排序", "Kahn 入度法与 DFS 三色法、环检测、按字典序或分层输出、课程表与外星字典。"),
 ("union-find", "并查集", "路径压缩 + 按秩合并、连通分量、动态加边、等价关系；和 BFS/DFS 的取舍。"),
 ("shortest-path", "最短路：Dijkstra 与其变体", "非负权 Dijkstra 的堆实现、0-1 BFS、带状态的最短路（剩余次数、方向）、Bellman-Ford 限制边数。"),
 ("backtracking", "回溯", "子集、组合、排列、分割、N 皇后的统一模板；选择 / 撤销、剪枝、去重（排序后跳过同层相同值）。"),
 ("dp-linear", "动态规划：线性与状态机", "爬楼梯、打家劫舍、最大子数组、买卖股票的状态机；定义状态、转移、初值、遍历顺序四步。"),
 ("dp-grid-string", "动态规划：网格、双串与区间", "路径计数、最长公共子序列、编辑距离、回文子串、区间 DP；二维状态的空间压缩。"),
 ("dp-knapsack", "动态规划：背包与计数", "0-1 背包与完全背包的遍历方向、组合数与排列数的区别、零钱兑换、目标和；记忆化搜索与递推的互换。"),
 ("greedy", "贪心", "交换论证、按某个键排序后一次扫描、跳跃游戏、分发糖果；怎样判断贪心是否成立、什么时候要退回 DP。"),
 ("trie", "字典树", "前缀查询、单词搜索 II、按前缀自动补全、异或最大值的位字典树；用 dict 嵌套的 Python 写法。"),
 ("design", "数据结构设计题", "LRU / LFU、带过期的缓存、时间相关的键值存储、随机集合 O(1)、迭代器设计；先定接口与复杂度目标。"),
 ("string-parsing", "字符串处理与表达式解析", "计算器（栈处理优先级与括号）、解码字符串、比较版本号、KMP / 滚动哈希的使用场景。"),
 ("math-bit-sim", "数学、位运算与模拟", "取模与溢出、最大公约数、快速幂、位运算技巧（lowbit、异或去重）、矩阵螺旋与旋转、按规则模拟。"),
]


def leaf_title(p):
    zh = p.get("title_zh") or ""
    if p.get("kind") == "variant":
        return zh
    if p.get("kind") == "supplement":
        return f"{p['fid']} {zh}"
    if p.get("kind") == "lcof":
        return f"{p['fid']} {zh}"
    return f"LC {p['id']} {zh}（{p['title']}）" if zh and zh != p["title"] else f"LC {p['id']} {p['title']}"


def leaf_summary(p):
    rep = p["companies"].get("reports")
    if rep:
        kind = "TikTok 变体题" if p.get("kind") == "variant" else "LeetCode 原题"
        return f"{kind}；近一年被问 {rep['refs']} 次、最近 {rep['last_seen'] or '日期不明'}。"
    cn = p["companies"].get("bytedance_cn")
    cn_txt = f"国内字节被问 {cn['reports']} 次、最近 {cn['last_seen']}" if cn else ""
    if "tiktok" not in p["companies"] and "bytedance" not in p["companies"]:
        return f"{p['difficulty'] or '—'}；{cn_txt}。"
    who = "、".join(f"{'TikTok' if c == 'tiktok' else '字节'} {v['freq']}" for c, v in p["companies"].items() if c in ("tiktok", "bytedance"))
    recent = {"30d": "；近 30 天出现", "3m": "；近 3 个月出现", "6m": "；近 6 个月出现"}.get(p.get("window", ""), "")
    cn_part = f"；{cn_txt}" if cn else ""
    return f"{p['difficulty']}；频率 {who}{recent}{cn_part}；{', '.join(p['tags'][:5])}。"


def branch(i, bid, title, summary, leaves, core):
    n = {"id": bid, "order": i, "title": title, "summary": summary}
    if core:
        n["core"] = True
    n["children"] = leaves
    return n


problems = list(index.values())
nodes = [
 branch(1, "python", "Python 面试工具箱", "刷题时最常用的标准库与写法：什么时候用、复杂度多少、哪里会踩坑。", 
        [{"id": f"python.{a}", "title": t, "summary": s} for a, t, s in PYTHON], True),
 branch(2, "patterns", "模式识别", "从题面信号到解法模式：每个模式的触发信号、Python 模板、正确性来源、常见变形与陷阱。",
        [{"id": f"patterns.{a}", "title": t, "summary": s} for a, t, s in PATTERNS], True),
 branch(3, "a", "A 档：最高频", "TikTok、字节（美国与国内）最高频的题：近半年出现、频率 ≥ 70，或国内被问 ≥ 50 次 / 近 30 天出现；按热度降序。",
        [{"id": f"a.{p['slug']}", "title": leaf_title(p), "summary": leaf_summary(p)} for p in problems if p["tier"] == "A"], True),
 branch(4, "b", "B 档：次高频", "频率 ≥ 50，或国内被问 ≥ 20 次 / 近 3 个月出现；按热度降序。",
        [{"id": f"b.{p['slug']}", "title": leaf_title(p), "summary": leaf_summary(p)} for p in problems if p["tier"] == "B"], False),
]
sk = {"domain": "tiktok-lc", "title": "TikTok 字节高频 LeetCode · 整题答案",
      "deck": "LeetCode Tops::24 TikTok 字节高频 · 整题答案（whole answers）",
      "lang": "zh", "vault": "interviews/core/leetcode/tiktok",
      "study": {"order": "core-first", "mix": "new-first", "new_per_day": 30, "reviews_per_day": 200},
      "nodes": nodes}
drill = {"domain": "tiktok-lc-drill", "title": "TikTok 字节高频 LeetCode · 拆分背诵",
         "deck": "LeetCode Tops::25 TikTok 字节高频 · 拆分背诵（split cards）",
         "lang": "zh", "vault": "interviews/core/leetcode/tiktok-drill",
         "study": {"order": "core-first", "mix": "new-first", "new_per_day": 40, "reviews_per_day": 250},
         "nodes": [{**n, "order": i} for i, n in enumerate(nodes[2:], 1)]}
hdr = ("# TikTok + ByteDance top-frequency LeetCode. Two decks under LeetCode Tops: {which}. Generated by\n"
       "# research/companies/tiktok/tools/gen_skeleton.py from index.json; re-run to regenerate.\n")
for data, name, which in ((sk, "tiktok-lc", "24 = one whole-answer card per problem plus the Python toolkit and "
                           "pattern branches (read first)"),
                          (drill, "tiktok-lc-drill", "25 = the same problems as 4-5 split cards each (warm-up)")):
    (ROOT / f"skeleton/{name}.yaml").write_text(
        hdr.format(which=which) + yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")
print(sum(len(n["children"]) for n in nodes), "leaves;", sum(len(n["children"]) for n in drill["nodes"]), "drill leaves")
