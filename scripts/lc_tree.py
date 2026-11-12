"""The LeetCode knowledge tree: 灵茶山艾府 (0x3F)'s problem lists, three levels deep, with our problems hung on it.

    uv run python scripts/lc_tree.py          # writes sources/local/lc/tree.json and prints the tree with counts

Levels: list (滑动窗口与双指针 …) -> group (定长滑窗 …) -> section (基础, 进阶 …), in 0x3F's own order, the lists in the
order he recommends studying them. The sections and their problem numbers come from sources/local/lc/0x3f/categories.json
(local only: third-party data). A problem listed in several sections is hung on the one in the list of its main
technique, else on the first. A problem in no list goes to 「未收录」 at the end of the list of its main technique, in a
section named after that technique. Inside a section problems are ordered by asked-frequency (importance).
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LC = ROOT / "sources/local/lc"

# the order 0x3F recommends; 链表、二叉树与回溯 is one stage of his, kept as its separate lists here
ORDER = ["滑动窗口/双指针", "二分算法", "单调栈", "网格图", "位运算", "图论", "动态规划", "数据结构", "数学", "贪心与思维",
         "链表", "二叉树", "一般树", "回溯", "递归/分治", "字符串"]
NAME = {"滑动窗口/双指针": "滑动窗口与双指针", "贪心与思维": "贪心与思维", "数据结构": "常用数据结构"}

# section -> group, per list, following the § headings of the original posts; a section not named here is its own group
GROUPS = {
    "滑动窗口/双指针": {"定长滑窗": ["定长滑窗基础", "定长滑窗进阶"],
                  "不定长滑窗": ["不定长滑窗 求最长", "不定长滑窗 求最短", "不定长滑窗 子数组个数", "滑窗其他"],
                  "单序列双指针": ["反转字符串", "相向双指针", "同向双指针", "背向双指针", "原地修改", "矩阵上的双指针"],
                  "双序列双指针": ["双序列双指针", "判断子序列"]},
    "二分算法": {"二分查找": ["二分查找基础"],
             "二分答案": ["二分答案 求最小", "二分答案 求最大", "二分间接值", "最小化最大值", "最大化最小值", "第 K 小/大"]},
    "单调栈": {"单调栈": ["基础", "进阶", "矩形", "贡献法", "最小字典序"]},
    "位运算": {"基础与性质": ["基础", "异或性质", "与或性质"], "技巧": ["拆位/贡献法", "试填法", "恒等式", "线性基", "思维", "位运算其他"]},
    "图论": {"DFS 与 BFS": ["图 DFS", "图 BFS", "图论建模 BFS", "跳跃游戏"], "拓扑排序": ["拓扑排序", "拓扑序上DP", "基环树"],
           "最短路": ["Dijkstra", "Floyd"], "其他图论": ["最小生成树", "欧拉路径", "强/双连通分量", "二分图染色", "网络流", "图论其他"]},
    "动态规划": {"入门": ["爬楼梯", "打家劫舍", "最大子数组和"], "网格": ["网格 DP 基础", "网格 DP 进阶"],
             "背包": ["0-1 背包", "完全背包", "多重背包", "分组背包", "树上背包"], "经典线性": ["最长公共子序列 LCS", "最长递增子序列 LIS"],
             "划分型": ["划分型 DP"], "状态机": ["股票买卖", "状态机 DP"], "其他线性": ["其他线性 DP", "多维 DP"],
             "区间": ["区间 DP"], "状压": ["状压 DP"], "数位与计数": ["数位 DP", "计数 DP", "DP 优化"],
             "树与图": ["树形 DP", "图 DP"], "博弈与概率": ["博弈 DP", "概率/期望 DP"]},
    "数据结构": {"常用枚举": ["枚举右维护左", "枚举中间", "遍历对角线"],
             "前缀和": ["前缀和 基础", "前缀和+哈希", "距离和", "状压前缀和", "前缀和进阶", "二维前缀和"],
             "差分": ["一维差分", "二维差分"], "栈": ["栈 基础", "栈 进阶", "邻项消除", "合法括号", "表达式解析", "对顶栈"],
             "队列": ["队列 基础", "队列 设计", "双端队列", "单调队列"],
             "堆": ["堆基础", "堆进阶", "堆 第K小/大", "堆 重排", "反悔堆", "懒删除堆", "对顶堆"],
             "字典树": ["字典树 基础", "字典树 进阶", "字典树优化DP", "0-1 字典树"],
             "并查集": ["并查集 基础", "并查集 进阶", "中介并查集", "数组上的并查集", "区间并查集", "带权并查集"],
             "树状数组与线段树": ["树状数组", "逆序对", "线段树"], "其他": ["根号算法", "离线算法"]},
    "数学": {"数论": ["判断质数", "筛质数", "质因数分解", "阶乘分解", "因子", "GCD", "LCM", "互质", "同余", "数论其他"],
           "组合数学": ["乘法原理", "组合计数", "容斥原理", "生成函数"], "概率与博弈": ["概率期望", "博弈论"],
           "计算几何": ["计算几何 点线", "计算几何 圆", "计算几何 矩形", "凸包"], "杂项": ["随机", "回文数", "整数拆分", "曼哈顿距离", "数学其他"]},
    "贪心与思维": {"贪心策略": ["从最小/最大开始", "单序列配对", "双序列配对", "从最左/最右开始", "划分型贪心", "先枚举再贪心", "交换论证法", "相邻不同", "反悔贪心"],
              "区间贪心": ["不相交区间", "区间分组", "区间选点", "区间覆盖", "合并区间", "区间其他"],
              "字符串与数学贪心": ["字符串贪心", "回文串贪心", "数学贪心"],
              "思维": ["从特殊到一般", "脑筋急转弯", "等价转化", "逆向思维", "贡献法", "两次扫描", "交换元素", "分类讨论"],
              "构造与其他": ["构造题", "交互题", "贪心其他"]},
    "链表": {"基础操作": ["遍历链表", "删除节点", "插入节点", "反转链表"], "指针技巧": ["前后指针", "快慢指针", "双指针"],
           "合并与分治": ["合并链表", "分治"], "综合": ["综合应用", "其他"]},
    "二叉树": {"遍历与 DFS": ["遍历二叉树", "自顶向下 DFS", "自底向上 DFS", "自底向上 DFS：删点", "有递有归", "二叉树的直径", "回溯", "最近公共祖先"],
            "二叉搜索树": ["二叉搜索树", "创建二叉树", "插入/删除节点"], "树形 DP 与 BFS": ["树形 DP", "二叉树 BFS"],
            "其他": ["链表+二叉树", "N 叉树", "其他"]},
    "回溯": {"回溯": ["入门回溯", "子集型回溯", "划分型回溯", "组合型回溯", "排列型回溯", "有重复元素的回溯"], "搜索": ["搜索", "折半搜索"]},
    "字符串": {"匹配": ["KMP", "Z 函数", "Manacher", "字符串哈希"], "其他": ["最小表示法", "AC 自动机", "后缀数组", "子序列自动机", "字符串其他"]},
}
# our technique patterns -> the 0x3F list a problem in no list joins
PATTERN_LIST = {"01-hashing": "数据结构", "02-prefix-sum": "数据结构", "03-two-pointers": "滑动窗口/双指针", "04-sliding-window": "滑动窗口/双指针",
                "05-monotonic-stack": "单调栈", "06-binary-search": "二分算法", "07-heap": "数据结构", "08-intervals": "贪心与思维",
                "09-linked-list": "链表", "10-tree-dfs": "二叉树", "11-tree-bfs-bst": "二叉树", "12-graph": "图论", "13-topo-sort": "图论",
                "14-union-find": "数据结构", "15-shortest-path": "图论", "16-backtracking": "回溯", "17-dp": "动态规划", "18-greedy": "贪心与思维",
                "19-trie": "数据结构", "20-design": "数据结构", "21-string": "字符串", "22-math-bit": "数学"}
UNLISTED = "未收录"


def build() -> dict:
    cats = json.loads((LC / "0x3f/categories.json").read_text(encoding="utf-8"))["CATEGORIES"]
    analysis = json.loads((LC / "analysis.json").read_text(encoding="utf-8"))
    probs = analysis["problems"]
    tech = {t["id"]: t for t in json.loads((LC / "taxonomy.json").read_text(encoding="utf-8"))["techniques"]}

    def own_list(p: dict) -> str | None:
        t = tech.get(p["techniques"][0]) if p["techniques"] else None
        return PATTERN_LIST.get(t["pattern"] if t else (p["patterns"] or [""])[0])

    places = defaultdict(list)  # LC number -> (list, section) in 0x3F order
    for lst in ORDER:
        for sec, nums in cats.get(lst, {}).items():
            for n in nums:
                places[n].append((lst, sec))
    hung: dict[tuple[str, str], list[str]] = defaultdict(list)
    for p in sorted(probs.values(), key=lambda p: -p["importance"]):
        found = places.get(p.get("num"), [])
        mine = own_list(p)
        if found:
            lst, sec = next((x for x in found if x[0] == mine), found[0])
        else:
            t = tech.get(p["techniques"][0]) if p["techniques"] else None
            lst, sec = mine or "数据结构", f"{UNLISTED} · {t['name'].split('（')[0] if t else '其他'}"
        hung[(lst, sec)].append(p["slug"])
    tree, primary = [], {}
    for lst in ORDER:
        groups = GROUPS.get(lst, {})
        group_of = {s: g for g, ss in groups.items() for s in ss}
        out: dict[str, list] = {}
        sections = list(cats.get(lst, {})) + sorted(s for (lst2, s) in hung if lst2 == lst and s.startswith(UNLISTED))
        for sec in sections:
            slugs = hung.get((lst, sec), [])
            g = UNLISTED if sec.startswith(UNLISTED) else group_of.get(sec, sec)
            out.setdefault(g, []).append({"name": sec.removeprefix(f"{UNLISTED} · "), "problems": slugs})
            for s in slugs:
                primary[s] = [NAME.get(lst, lst), g, sec]
        tree.append({"name": NAME.get(lst, lst), "groups": [{"name": g, "sections": ss} for g, ss in out.items()]})
    return {"lists": tree, "primary": primary}


def main() -> int:
    t = build()
    (LC / "tree.json").write_text(json.dumps(t, ensure_ascii=False, indent=1), encoding="utf-8")
    for lst in t["lists"]:
        n = sum(len(s["problems"]) for g in lst["groups"] for s in g["sections"])
        print(f"{lst['name']}  {n}")
        for g in lst["groups"]:
            secs = [f"{s['name']} {len(s['problems'])}" for s in g["sections"] if s["problems"]]
            if secs:
                print(f"  {g['name']}: " + " · ".join(secs))
    print(f"{len(t['primary'])} problems placed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
