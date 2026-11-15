---
slug: reachable-nodes-with-restrictions
---
## Q
**LC 2368 受限条件下可到达节点的数目**｜Medium

`n` 个点的无向树和受限点集合（不含 0），不经过受限点，从 0 出发最多能到达几个点。

## A
**一句话。** 从 0 做 DFS，遇到受限点就不进去；树上只需记父结点防止走回头路，返回能到达的点数。

```python
def reachable_nodes(n, edges, restricted):
    g = [[] for _ in range(n)]
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)
    banned = set(restricted)

    def dfs(u, fa):            # u 下面能到达的点数（含 u）
        cnt = 1
        for v in g[u]:
            if v != fa and v not in banned:
                cnt += dfs(v, u)
        return cnt

    return dfs(0, -1)
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 用列表判断受限：`v in restricted` 每次 `O(k)`，要转成集合。
- 链状树递归深达 `10^5`：CPython 要调高递归上限或改用 BFS。

**追问。**
- 不建图？：并查集合并所有两端都不受限的边，答案是 0 所在集合的大小。
- 为什么树上不用 `visited`？：无环，只要不回到父结点就不会重复访问。

**同模式。** LC 200 岛屿数量、LC 841 钥匙和房间、LC 1971 寻找图中是否存在路径
