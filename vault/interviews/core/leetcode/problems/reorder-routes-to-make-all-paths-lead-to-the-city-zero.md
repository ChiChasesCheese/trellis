---
slug: reorder-routes-to-make-all-paths-lead-to-the-city-zero
---
## Q
**LC 1466 重新规划路线**｜Medium

`n` 座城市由 `n-1` 条有向路线连成一棵树，最少反转几条路线，才能让每座城市都能到达城市 `0`。

## A
**一句话。** 把有向边当无向边建图，顺着原方向的边标 `1`（背离 `0`，要反转），逆着的标 `0`，从 `0` 遍历累加标记。

```python
def min_reorder(n, connections):
    adj = [[] for _ in range(n)]
    for a, b in connections:
        adj[a].append((b, 1))    # 顺原方向走，背离 0，要反转
        adj[b].append((a, 0))    # 逆原方向走，朝向 0，不用动
    def dfs(u, parent):
        flips = 0
        for v, cost in adj[u]:
            if v != parent:      # 树无环，不走回父亲即可
                flips += cost + dfs(v, u)
        return flips
    return dfs(0, -1)
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 只沿出边遍历：到不了的城市整个漏掉，示例 `[[1,0],[1,2],[3,2],[3,4]]` 得 `0`，应为 `2`。
- 标记写反：`[[1,0],[2,0]]` 本该是 `0`，写反得 `2`。
- 链状树深 `5*10^4` 会 `RecursionError`，要调大递归上限或用显式栈加 `seen`。

**追问。**
- 反过来要城市 `0` 能到达所有城市？：答案是 `n - 1` 减原答案。
- 一般有向图求 `s` 到 `t` 最少反转几条边？：顺向代价 `0`、逆向代价 `1`，用 `0-1 BFS`。

**同模式。** LC 1971 寻找图中是否存在路径、LC 310 最小高度树、LC 1376 通知所有员工所需的时间、LC 834 树中距离之和
