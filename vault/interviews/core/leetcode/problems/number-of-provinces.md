---
slug: number-of-provinces
---
## Q
**LC 547 省份数量**｜Medium

有 `n` 个城市，其中一些彼此直接相连，另一些没有。若城市 `a` 与 `b` 直接相连、`b` 与 `c` 直接相连，则 `a` 与 `c` 间接相连。「省份」是一组直接或间接相连的城市，组内不含其他没有相连的城市。给你 `n x n` 的矩阵 `isConnected`，`isConnected[i][j] = 1` 表示城市 `i` 和 `j` 直接相连，`0` 表示不直接相连。返回省份的数量。`1 <= n <= 200`，`isConnected[i][j]` 为 `1` 或 `0`，`isConnected[i][i] == 1`，`isConnected[i][j] == isConnected[j][i]`。例：`[[1,1,0],[1,1,0],[0,0,1]]` → `2`；`[[1,0,0],[0,1,0],[0,0,1]]` → `3`。同一道题也常被包装成「朋友圈有几个」「相似照片分成几组」。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 求无向图的连通分量（connected component）个数：对每个还没访问过的城市做一次递归 DFS，把它能到达的城市全部标记，DFS 的启动次数就是省份数。`O(n^2)` 时间，`O(n)` 空间。

**识别。** 「直接或间接相连」是传递闭包（transitive closure），「一组互相可达的」就是连通分量；矩阵以邻接矩阵（adjacency matrix）的形式给出，顶点是城市，不是格子。朋友圈、相似照片分组、账号合并都是同一个模型。`n <= 200`：读一遍矩阵 `O(n^2)` 也只有 `4 * 10^4`，任何线性于边数的算法都够。

**推导。** 暴力：对每个城市各搜一遍可达城市再去重，同一个省份被搜很多次。洞察：一个省份搜一次就够，所以访问过的城市立刻标记，外层循环跳过已标记的城市；新启动一次 DFS 就多一个省份。

```python
def find_circle_num(is_connected: list[list[int]]) -> int:
    n = len(is_connected)
    seen = [False] * n

    def dfs(i: int) -> None:                      # 把 i 所在省份的所有城市标记为已访问
        seen[i] = True                            # 先标记再递归，否则 i 和邻居会来回调用
        for j in range(n):
            if is_connected[i][j] and not seen[j]:
                dfs(j)

    provinces = 0
    for i in range(n):
        if not seen[i]:                           # 没被前面任何一次 DFS 到达：一个新省份
            dfs(i)
            provinces += 1
    return provinces
```

运行：`[[1,1,0],[1,1,0],[0,0,1]]` → `2`，`[[1,0,0],[0,1,0],[0,0,1]]` → `3`；`[[1]]` → `1`，`[[1,1],[1,1]]` → `1`；`n = 200` 全为 `1` → `1`，`n = 200` 只有对角线为 `1` → `200`，`n = 200` 的链 `0-1-2-...-199` → `1`。

**复杂度。** 时间 `O(n^2)`：每个城市恰好进入一次 DFS，进入后扫一行 `n` 个格子；空间 `O(n)`：`seen` 加递归栈，栈深最多 `n`。

**拓展优化。**
- 并查集（union-find）：初始每个城市自成一个集合（`n` 个省份），每合并两个不同集合就少一个省份。不递归，也适合边一条条在线加入的场景。

```python
def find_circle_num_uf(is_connected: list[list[int]]) -> int:
    n = len(is_connected)
    parent = list(range(n))                       # parent[x] == x 表示 x 是所在集合的根

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]         # 路径折半，让后续查找更快
            x = parent[x]
        return x

    provinces = n                                 # 起点：每个城市一个省份
    for i in range(n):
        for j in range(i + 1, n):                 # 矩阵对称，只看上三角
            if is_connected[i][j]:
                root_i, root_j = find(i), find(j)
                if root_i != root_j:              # 两个不同省份被连起来：省份数减一
                    parent[root_i] = root_j
                    provinces -= 1
    return provinces
```

`[[1,1,0],[1,1,0],[0,0,1]]` → `2`；时间 `O(n^2 · α(n))`，空间 `O(n)`。

**易错点。**
- 把 `isConnected` 当网格做上下左右的岛屿 DFS：`[[1,0,1],[0,1,0],[1,0,1]]` 在网格里是 `5` 块，正确答案是 `2`（城市 `0` 和 `2` 相连，城市 `1` 单独一个）；邻居是 `j in range(n)` 里 `isConnected[i][j] == 1` 的城市。
- 先递归、后标记 `seen`：`dfs(0)` 里 `isConnected[0][0] == 1` 且 `0` 还没标记，立刻再调 `dfs(0)`，连 `[[1]]` 都会无限递归，正确是 `1`；标记必须是 `dfs` 的第一句。
- 递归深度：最坏是一条链，深度等于 `n`；`n <= 200` 没有问题，但 `n` 超过约 `1000`（CPython 默认递归上限）会抛 `RecursionError`，要调高 `sys.setrecursionlimit` 或者写成迭代。

**追问。**
- 城市很多、不能递归：换成显式栈，入栈时就标记，`O(n^2)` 时间，没有递归深度限制。

```python
def find_circle_num_stack(is_connected: list[list[int]]) -> int:
    n = len(is_connected)
    seen = [False] * n
    provinces = 0
    for start in range(n):
        if seen[start]:
            continue
        provinces += 1
        seen[start] = True                        # 入栈时就标记，每个城市只入栈一次
        stack = [start]
        while stack:
            i = stack.pop()
            for j in range(n):
                if is_connected[i][j] and not seen[j]:
                    seen[j] = True
                    stack.append(j)
    return provinces
```

- 输入是边列表而不是矩阵，或者边在线到来（每来一条边问当前省份数）：并查集，每条边 `O(α(n))`。
- 要输出每个省份里有哪些城市：并查集结束后按 `find(i)` 分组，或 DFS 里把访问到的城市收集进列表。

**同模式。** LC 200 岛屿数量、LC 323 无向图中连通分量的数目、LC 684 冗余连接、LC 721 账户合并、LC 1319 连通网络的操作次数。
