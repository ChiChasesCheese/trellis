---
id: tlc-tops-alien-dictionary-0-whole
node: graphs.alien-dictionary
type: qa
---
## Q
**LC 269 Alien Dictionary**｜Hard · 全公司热度第 99 名 · Blind 75、NeetCode 150

有一种使用英语小写字母的外星语言，字母顺序未知。给你字符串列表 `words`，其中的单词已经按这门语言的字典序排好。如果这个说法是错的、`words` 不对应任何字母顺序，返回 `""`；否则返回一个按该语言规则字典递增排列的、包含所有出现过字母的字符串，有多个解时返回任意一个。`1 <= words.length <= 100`，`1 <= words[i].length <= 100`，`words[i]` 仅由小写字母组成。

例：`words = ["wrt","wrf","er","ett","rftt"]` → `"wertf"`；`words = ["z","x"]` → `"zx"`；`words = ["z","x","z"]` → `""`（`z` 既在 `x` 前又在 `x` 后）。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点：** 从有序样本恢复未知顺序：相邻单词第一个不同的字母建有向边，再拓扑排序（topological sort）；有环或前缀违例则无解。

**一句话。** 只看相邻两个单词，第一个不同的字母 `x`（前词）、`y`（后词）给出约束「`x` 在 `y` 前」；所有字母是结点、约束是边，对图做拓扑排序，有环返回 `""`。

**识别。** 「已按某个未知顺序排好」「还原这个顺序」是偏序约束加拓扑排序的信号；「有多个解返回任意一个」说明只要一个合法线性化。无解有两种：约束成环，或「长词排在它的真前缀前面」。字母最多 26 个，规模不是问题，难点在建图。

**推导。** 暴力：枚举字母的全排列检查，`26!` 不可行。关键洞察：已排序序列有传递性，只有相邻两个单词需要比较，每对最多贡献一条边（第一个不同的字母），后面的字母没有信息。建图后做 DFS 拓扑排序：后序遍历里，一个字母要等它所有后继都入列之后才入列，把结果反转就是合法顺序；遍历中碰到「正在当前路径上」的字母就有环。

```python
from itertools import pairwise


def alien_order(words: list[str]) -> str:
    graph: dict[str, set[str]] = {c: set() for w in words for c in w}   # 出现过的每个字母都是结点
    for a, b in pairwise(words):            # 只有相邻两个词能提供约束
        for x, y in zip(a, b):
            if x != y:
                graph[x].add(y)             # 第一个不同的字母：x 排在 y 前面；集合自动去重
                break
        else:                               # 没有 break：a 是 b 的前缀或相同
            if len(a) > len(b):             # b 是 a 的真前缀却排在后面：非法
                return ""

    state: dict[str, int] = {}              # 缺省 = 未访问；1 在当前路径上；2 已完成
    order: list[str] = []

    def dfs(c: str) -> bool:                # 返回 False 表示发现环
        if state.get(c) == 1:
            return False
        if state.get(c) == 2:
            return True
        state[c] = 1
        for nxt in graph[c]:
            if not dfs(nxt):
                return False
        state[c] = 2
        order.append(c)                     # 后序：c 的所有后继都已经入列
        return True

    for c in graph:
        if not dfs(c):
            return ""
    return "".join(reversed(order))         # 后序反转 = 拓扑序
```

**运行。** `["wrt","wrf","er","ett","rftt"]` → `"wertf"`；`["z","x"]` → `"zx"`；`["z","x","z"]` → `""`；`["abc","ab"]` → `""`；`["z"]` → `"z"`；`["ab","adc"]` → `"cbda"`（只要求 `b` 在 `d` 前，其余字母顺序任意；多解时返回哪一个取决于遍历顺序）。

**复杂度。** 时间 `O(C + E)`，`C` 是所有单词字符总数，边数 `E <= 26 * 25`；空间 `O(26 + E)`。

**拓展优化。**
- 要字典序最小的合法顺序，或判断顺序是否唯一：改用 Kahn 算法，队列换成最小堆；队列任何时刻只有一个元素则顺序唯一。
```python
import heapq


def alien_order_smallest(words: list[str]) -> str:
    graph: dict[str, set[str]] = {c: set() for w in words for c in w}
    indeg = dict.fromkeys(graph, 0)
    for a, b in pairwise(words):
        for x, y in zip(a, b):
            if x != y:
                if y not in graph[x]:       # 重复边只计一次入度
                    graph[x].add(y)
                    indeg[y] += 1
                break
        else:
            if len(a) > len(b):
                return ""
    heap = [c for c, d in indeg.items() if d == 0]
    heapq.heapify(heap)
    out: list[str] = []
    while heap:
        c = heapq.heappop(heap)             # 每次取入度为 0 的最小字母
        out.append(c)
        for nxt in graph[c]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                heapq.heappush(heap, nxt)
    return "".join(out) if len(out) == len(graph) else ""
```
- 字母表很大（Unicode）：图换成按需建立的字典，复杂度仍线性。

**易错点。**
- 漏掉前缀情形：`["abc","ab"]` 里 `zip` 找不出不同的字母，没有边，会当作合法并返回一个字母排列（如 `"cba"`），正确是 `""`。`for … else` 正好处理没有 `break` 的情况。
- 只从边里收集字母：没有任何约束的字母丢失，`["z"]` 返回 `""` 而不是 `"z"`。所有出现过的字母要先登记为结点。
- DFS 只用一个 `visited`：环里的结点被当作已完成，`["z","x","z"]` 不会返回 `""`，而是输出 `"zx"`。必须区分「在路径上」和「已完成」。

**同模式。** LC 207 课程表、LC 210 课程表 II、LC 953 验证外星语词典、LC 444 序列重建。
