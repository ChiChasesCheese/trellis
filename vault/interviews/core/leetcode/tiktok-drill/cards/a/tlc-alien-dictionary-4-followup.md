---
id: tlc-alien-dictionary-4-followup
node: a.alien-dictionary
type: qa
step: 4
---
## Q
**LC 269 火星词典（Alien Dictionary）**｜追问

面试官接着问：（1）要求在所有合法顺序里返回字母序最小的那个？（2）怎样判断合法顺序是否唯一？（3）单词总量很大，但只有相邻词对有用，怎么省内存？

## A
1. **字母序最小。** Kahn 过程中把"当前入度为 `0` 的字母"放进最小堆，每次取最小的：

```python
from heapq import heapify, heappop, heappush
from itertools import pairwise


def alien_order_smallest(words: list[str]) -> str:
    graph: dict[str, set[str]] = {ch: set() for w in words for ch in w}
    indeg = dict.fromkeys(graph, 0)
    for a, b in pairwise(words):
        for x, y in zip(a, b):
            if x != y:
                if y not in graph[x]:
                    graph[x].add(y)
                    indeg[y] += 1
                break
        else:
            if len(a) > len(b):
                return ""
    heap = [ch for ch, d in indeg.items() if d == 0]
    heapify(heap)                                # 最小堆：每次取字母序最小的入度 0 字母
    order: list[str] = []
    while heap:
        ch = heappop(heap)
        order.append(ch)
        for nxt in graph[ch]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                heappush(heap, nxt)
    return "".join(order) if len(order) == len(graph) else ""
```

例 1 得 `"wertf"`。
2. **是否唯一。** 拓扑排序结果唯一，当且仅当整个过程中队列大小始终为 `1`（每一步都只有一个入度为 `0` 的候选）。
3. **省内存。** 只需要保留前一个单词，边读边处理相邻词对；图最多 `26 * 25` 条边，与单词总量无关。

**Python 提醒**：`heapq` 里放字符串按字典序比较；同一字母只会在入度归零时入堆一次，不需要去重。遍历 `graph[ch]`（集合）的顺序是任意的，只有堆保证了输出里的取舍顺序。
