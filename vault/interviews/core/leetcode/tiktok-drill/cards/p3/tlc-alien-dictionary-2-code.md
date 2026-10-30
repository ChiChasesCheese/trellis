---
id: tlc-alien-dictionary-2-code
node: p3.alien-dictionary
type: qa
step: 2
---
## Q
**LC 269 火星词典（Alien Dictionary）**｜写出 Python 实现

字符串列表 `words`（`1..100` 个，每个长度 `1..100`，只含小写字母），已知按某个未知字母顺序排好序。返回一个与之一致的字母顺序（包含所有出现过的字母，任意一个），若自相矛盾返回 `""`。

## A
**思路。** 先登记所有出现过的字母为结点。对相邻单词 `zip` 比较，第一个不同的字母对 `(x, y)` 建边 `x → y`（用集合去重，入度只在新增边时加一）；若 `zip` 走完都相同且前词更长，说明违反前缀规则，返回 `""`。然后用 Kahn 算法拓扑排序，取出的字母数少于总数就说明有环。

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

**运行。** `["wrt","wrf","er","ett","rftt"]` → `"wertf"`；`["z","x"]` → `"zx"`；`["z","x","z"]` → `""`；`["abc","ab"]` → `""`；`["z"]` → `"z"`；`["ab","adc"]` → `"abcd"`。

**复杂度。** 时间 `O(C + E)`，`C` 为总字符数，`E <= 26 * 25`；空间 `O(26 + E)`。

**写法要点。** 字典推导 `{ch: set() for w in words for ch in w}` 一次登记所有字母，同时因为字典保持插入顺序，输出稳定；`dict.fromkeys(graph, 0)` 按同样的键建入度表；`itertools.pairwise` 取相邻词对；`zip(a, b)` 在较短者处自动停止；`for … else` 的 `else` 只在没有 `break` 时执行，正好表示"两个词在较短者的长度内完全相同"；`deque` 做队列，`popleft` 是 `O(1)`。
