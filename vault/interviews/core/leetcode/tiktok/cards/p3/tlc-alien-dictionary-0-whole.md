---
id: tlc-alien-dictionary-0-whole
node: p3.alien-dictionary
type: qa
---
## Q
**LC 269 火星词典（Alien Dictionary）**｜Hard · LC TikTok 热度 53/100 · 近一年被问：美国 4 次、国内 0 次 · CodeTop 国内累计 2 次 · 最近 2026-09-02（面试记录）

有一种使用英语小写字母的外星语言，字母顺序未知。给你字符串列表 `words`，其中的单词已经**按这门语言的字典序排好**。如果这个说法是错的、`words` 不对应任何字母顺序，返回 `""`；否则返回一个按该语言规则字典递增排列的、包含所有出现过字母的字符串，有多个解时返回任意一个。`1 <= words.length <= 100`，`1 <= words[i].length <= 100`，`words[i]` 仅由小写字母组成。例：`["wrt","wrf","er","ett","rftt"]` → `"wertf"`；`["z","x"]` → `"zx"`；`["z","x","z"]` → `""`（`z` 既在 `x` 前又在 `x` 后）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 只看相邻两个单词：第一个不同的字母 `x`（前词）、`y`（后词）给出一条约束「`x` 排在 `y` 前」；所有出现过的字母是图的结点，约束是有向边，对图做拓扑排序（Kahn 算法）；排不完（有环）或出现「长词是短词的真前缀却排在前面」就返回 `""`。`O(C)`，`C` 是所有字符总数。

**识别。** 「已按未知顺序排好的序列，恢复这个顺序」是偏序约束加拓扑排序的信号：序列给出的是字母之间的「先于」关系，不是完整顺序。「任意一个解」说明只要求一个合法的线性化。无解有两种：约束成环，或者前缀违例。

**推导。** 暴力：枚举字母的全排列检查，最坏 `26!`。洞察：已排序序列的传递性意味着只有**相邻**两个单词需要比较，每对最多贡献一条边（第一个不同的字母），其余字母位置没有信息。建图后，入度为 `0` 的字母可以放在最前面，取走后更新邻居入度，重复；全部取完就是一个合法顺序，取不完说明有环。

```python
from collections import deque
from itertools import pairwise


def alien_order(words: list[str]) -> str:
    graph: dict[str, set[str]] = {ch: set() for w in words for ch in w}   # 出现过的每个字母都是结点
    indeg = dict.fromkeys(graph, 0)
    for a, b in pairwise(words):                 # 只有相邻两个词能提供约束
        for x, y in zip(a, b):
            if x != y:                           # 第一个不同的字母：x 排在 y 前面
                if y not in graph[x]:
                    graph[x].add(y)
                    indeg[y] += 1
                break
        else:
            if len(a) > len(b):                  # b 是 a 的真前缀却排在后面：非法
                return ""
    queue = deque(ch for ch, d in indeg.items() if d == 0)
    order: list[str] = []
    while queue:                                 # Kahn 拓扑排序
        ch = queue.popleft()
        order.append(ch)
        for nxt in graph[ch]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                queue.append(nxt)
    return "".join(order) if len(order) == len(graph) else ""   # 没排完说明有环
```

**运行。** 例 1 → `"wertf"`；例 2 → `"zx"`；例 3 → `""`；`["abc","ab"]` → `""`；`["z"]` → `"z"`；`["ab","adc"]` → `"abcd"`；`["a","b","a"]` → `""`；`["ab","ab"]` → `"ab"`。

**复杂度。** 时间 `O(C + E)`：扫描所有相邻词对共 `O(C)`，边数 `E <= 26 * 25`；空间 `O(26 + E)`。

**易错点。**
- 漏掉前缀情形：`["abc","ab"]` 里 `zip` 比较不出任何不同字母，没有边，会返回 `"abc"`；正确是 `""`，因为长词不能排在它的前缀前面。`for … else` 正好处理这种「没有 `break`」的情况。
- 只从边里收集字母，会丢掉没有任何约束的字母：`["z"]` 必须返回 `"z"`。所有出现过的字母要先登记为结点。
- 重复的边既加入度又不去重：`["ab","ac","xb","xc"]` 里 `b → c` 出现两次，`indeg['c']` 变成 `2`，而邻接集合里只有一条边，减一次永远到不了 `0`，错误返回 `""`。边要先判重再计入度。

**追问。**
- 要字典序最小的合法顺序：把队列换成最小堆（`heapq`），每次取入度为 `0` 的最小字母。
- 判断合法顺序是否唯一：Kahn 过程中，队列任何时候都只有一个元素，则唯一。
- 字母表很大（Unicode）：图换成按需建立的字典即可，复杂度仍然线性。

**同模式。** LC 207 课程表、LC 210 课程表 II、LC 953 验证外星语词典、LC 444 序列重建、LC 1203 项目管理。
