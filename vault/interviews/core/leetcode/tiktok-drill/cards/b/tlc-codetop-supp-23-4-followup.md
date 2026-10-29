---
id: tlc-codetop-supp-23-4-followup
node: b.codetop-supp-23
type: qa
step: 4
---
## Q
**补充题23 检测循环依赖**｜追问

面试官接着问：（1）发现有环后，要把这个环具体打印出来？（2）Python 标准库里有没有现成的？（3）依赖是一条一条在线加入的，怎么在加入前拒绝会成环的依赖？

## A
1. **输出一个环。** 沿“依赖”方向（`a -> b`）做迭代 DFS，节点三色：`0` 未访问、`1` 在当前路径上、`2` 已完成；遇到颜色为 `1` 的点，说明路径上从该点起的一段就是环：
```python
def find_cycle(n: int, deps: list[list[int]]) -> list[int]:
    graph: list[list[int]] = [[] for _ in range(n)]
    for a, b in deps:
        graph[a].append(b)                  # 沿“依赖”方向走：a -> b
    color = [0] * n                         # 0 未访问，1 在当前路径上，2 已完成
    for s in range(n):
        if color[s]:
            continue
        path = [s]
        its = [iter(graph[s])]
        color[s] = 1
        while its:
            for v in its[-1]:
                if color[v] == 1:           # 撞上当前路径上的点：路径从 v 起的一段就是环
                    return path[path.index(v):] + [v]
                if color[v] == 0:
                    color[v] = 1
                    path.append(v)
                    its.append(iter(graph[v]))
                    break
            else:
                color[path.pop()] = 2
                its.pop()
    return []
```
`find_cycle(4, [[1,0],[2,1],[3,2],[0,3]])` → `[0, 3, 2, 1, 0]`，无环时返回 `[]`。用迭代器栈代替递归，`10^5` 层也不会超出递归上限。
2. **标准库 `graphlib`。** `TopologicalSorter` 接收「节点 → 它的前置集合」的字典，这与“`a` 依赖 `b`”的方向一致：`graph[a].add(b)`。有环时 `prepare()` 或 `static_order()` 抛 `CycleError`，`e.args[1]` 就是一个环：`{0: {1}, 1: {2}, 2: {0}}` 得到 `[0, 2, 1, 0]`；无环时 `static_order()` 给出合法构建顺序，`{1: {0}, 2: {1, 0}}` 得到 `(0, 1, 2)`。
3. **在线加边。** 新增 `[a, b]` 前，从 `b` 沿依赖方向搜索能否到达 `a`；能到达就拒绝，否则加入。单次 `O(n + m)`，频繁加边时可以用动态拓扑序等更复杂的结构。

**Python 提醒**：`graphlib` 的图是「节点到前置节点集合」，方向与大多数教材的邻接表（节点到后继）相反；传错方向不会报错，只会得到相反的构建顺序。
