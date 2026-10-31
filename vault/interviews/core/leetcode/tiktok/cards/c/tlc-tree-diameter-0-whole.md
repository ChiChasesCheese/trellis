---
id: tlc-tree-diameter-0-whole
node: c.tree-diameter
type: qa
---
## Q
**LC 1245 树的直径**｜Medium · LC TikTok 全时段热度 38/100 · CodeTop 国内累计 1 次 · 最近 2022-08-07（国内 CodeTop）

给一棵无向树，用边数组 `edges` 表示（`edges[i] = [u, v]` 是双向边），节点标记为 `0..edges.length` 且互不相同。返回这棵树的直径：树上最长简单路径的**边数**。`0 <= edges.length < 10^4`，`edges[i][0] != edges[i][1]`，`edges` 保证构成一棵无向树。例：`edges = [[0,1],[0,2]]` → `2`；`edges = [[0,1],[1,2],[2,3],[1,4],[4,5]]` → `4`（路径 `3-2-1-4-5`）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 任何最长路径都有一个最高点，DFS 求每个节点向下的最长两条分支，两者之和的最大值就是直径。

**识别。** 「树上最长路径」：枚举路径的最高点（转折点），经过它的最长路径等于它最长的两棵子树向下深度之和。同类问题（二叉树直径、最大路径和）都是这一套「递归返回单侧、更新全局答案用双侧」。

**推导。** 暴力：从每个节点出发 BFS 求最远距离，取最大，`O(n²)`，`n = 10^4` 约 `10^8`，偏慢。洞察：对节点 `u`，设各孩子的「向下高度 + 1」中最大的两个为 `top1`、`top2`，经过 `u` 的最长路径是 `top1 + top2`；`u` 返回给父亲的只能是单侧 `top1`。

```python
from collections import defaultdict


def tree_diameter(edges: list[list[int]]) -> int:
    graph: defaultdict[int, list[int]] = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    diameter = 0

    def height(node: int, parent: int) -> int:   # 返回 node 向下的最长路径边数
        nonlocal diameter
        top1 = top2 = 0                          # 孩子分支（含到孩子那条边）最长的两个
        for nxt in graph[node]:
            if nxt == parent:                    # 无向树：不能回头走向父亲
                continue
            h = height(nxt, node) + 1
            if h > top1:
                top1, top2 = h, top1
            elif h > top2:
                top2 = h
        diameter = max(diameter, top1 + top2)    # 以 node 为最高点的最长路径
        return top1                              # 对父亲只能贡献一条分支

    height(0, -1)
    return diameter
```

运行：`[[0,1],[0,2]]` → `2`，`[[0,1],[1,2],[2,3],[1,4],[4,5]]` → `4`，`[]`（只有节点 `0`）→ `0`，`[[0,1]]` → `1`。

**复杂度。** 时间 `O(n)`，空间 `O(n)`（邻接表加递归栈）。

**拓展优化。**
- 带权边：`h = height(...) + weight`，其余不变。
- 不关心路径具体经过哪里，只要长度：两次 BFS（见追问）同样 `O(n)`，且没有递归。

**易错点。**
- `top1` 与 `top2` 初始化为 `0` 而不是负无穷：叶子节点没有孩子，`top1 + top2 = 0` 正好是以它为端点的单节点路径。
- 返回 `top1 + top2` 给父亲：两条分支加在一起不是一条路径，父亲再接上去就拐了回头弯。
- 链状树深度 `10^4`：CPython 默认递归上限约 1000，会抛 `RecursionError`，要 `sys.setrecursionlimit` 调高或改用迭代。

**追问。**
- 为什么两次 BFS 对：从任意点出发最远的点一定是某条直径的端点；再从它出发最远的距离就是直径。迭代、无递归深度问题（不适用于负权）。

```python
from collections import defaultdict, deque


def tree_diameter_bfs(edges: list[list[int]]) -> int:
    graph: defaultdict[int, list[int]] = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    def farthest(start: int) -> tuple[int, int]:  # 返回 (最远的点, 距离)
        dist = {start: 0}
        queue = deque([start])
        last = start
        while queue:
            last = queue.popleft()               # BFS 出队顺序距离不减，最后一个就是最远的
            for nxt in graph[last]:
                if nxt not in dist:
                    dist[nxt] = dist[last] + 1
                    queue.append(nxt)
        return last, dist[last]

    end, _ = farthest(0)                         # 第一次：找到一条直径的端点
    return farthest(end)[1]                      # 第二次：从端点出发的最远距离就是直径
```

- 输出直径路径本身：BFS 时记录前驱 `prev`，从第二个端点回溯。

**同模式。** LC 543 二叉树的直径、LC 124 二叉树中的最大路径和、LC 687 最长同值路径、LC 310 最小高度树、LC 1522 N 叉树的直径。
