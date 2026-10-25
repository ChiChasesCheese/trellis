---
id: tlc-number-of-connected-components-in-an-undirected-graph-2-code
node: b.number-of-connected-components-in-an-undirected-graph
type: qa
step: 2
---
## Q
**LC 323 无向图中连通分量的数目**｜写出 Python 实现

`n` 个节点（`1 <= n <= 2000`）、无重复边的无向图，`edges` 最多 `5000` 条，`edges[i] = [a, b]`，`0 <= a <= b < n`，`a != b`。用并查集返回连通分量个数。

## A
**思路。** `parent` 数组初始每个点指向自己，计数 `comps = n`。逐条边找两端的根，根不同就把一个根挂到另一个根上，`comps` 减一。

```python
def count_components(n: int, edges: list[list[int]]) -> int:
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]      # 路径减半：顺手把 x 挂到祖父下面
            x = parent[x]
        return x

    comps = n
    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra != rb:                           # 两端本来不连通：合并一次，分量少一个
            parent[ra] = rb
            comps -= 1
    return comps
```

运行：`5, [[0,1],[1,2],[3,4]]` → `2`；`5, [[0,1],[1,2],[2,3],[3,4]]` → `1`；`1, []` → `1`；`4, []` → `4`；`n = 2000` 的链加 `5000` 条边在毫秒内得到 `1`。

**复杂度。** 时间 `O((n + m) α(n))`：每条边两次 `find`，路径压缩使其近似常数；空间 `O(n)`：`parent` 数组。

**写法要点。** `list(range(n))` 一行初始化 `parent[i] = i`；`find` 用 `while` 迭代，避免递归深度问题；`parent[x] = parent[parent[x]]` 是**路径减半**，只比完整压缩多走半步，却不需要第二个循环；`a, b` 直接在 `for` 里解包边。
