---
id: tlc-patterns-topo-sort-5-alien
node: patterns.topo-sort
type: qa
step: 5
---
## Q
**拓扑排序（Topological Sort）｜火星词典（LC 269）：怎样从排好序的单词建图**

给出已排序的单词列表，如何得到字母的顺序？有哪两个容易漏掉的非法 / 边界情况？

## A
**建边**：只比较**相邻**的两个单词，找到第一个不同的字母 `x != y`，得到 `x` 排在 `y` 前，边 `x -> y`，其后的字母不再提供信息。

```python
from collections import deque
def alien_order(words: list[str]) -> str:
    graph: dict[str, set[str]] = {ch: set() for w in words for ch in w}   # 所有出现过的字母都是节点
    indeg = {ch: 0 for ch in graph}
    for a, b in zip(words, words[1:]):
        if len(a) > len(b) and a.startswith(b):
            return ""                      # "abc" 排在 "ab" 前面：前缀反序，非法
        for x, y in zip(a, b):
            if x != y:
                if y not in graph[x]:
                    graph[x].add(y)
                    indeg[y] += 1
                break
    q = deque(ch for ch in graph if indeg[ch] == 0)
    out: list[str] = []
    while q:
        ch = q.popleft()
        out.append(ch)
        for nxt in graph[ch]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                q.append(nxt)
    return "".join(out) if len(out) == len(graph) else ""
print(alien_order(["wrt","wrf","er","ett","rftt"]), alien_order(["z","x"]), repr(alien_order(["z","x","z"])))   # wertf zx ''
```

- **前缀反序**：`["abc", "ab"]` 没有任何不同字母，却是非法的，必须单独判断；漏掉它会返回 `"abc"`，正确是 `""`。
- **孤立字母**：节点集合要包含所有出现过的字母，不是只有出现在边里的。`["a", "a"]` 只靠边建点会得到 `""`，正确是 `"a"`。
- 同一对 `(x, y)` 多次出现要去重，否则入度会被重复累加。
- 环（`["z","x","z"]` 给出 `z→x` 与 `x→z`）使输出长度不足 `V`，返回 `""`。
- 时间 `O(总字符数)`，节点最多 26 个。
