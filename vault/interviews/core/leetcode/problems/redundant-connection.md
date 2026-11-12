---
slug: redundant-connection
---
## Q
**LC 684 冗余连接（Redundant Connection）**｜Medium

一棵 `n` 个节点（编号 `1..n`）的树多加了一条边。返回可以删去使其重新成树的边，有多个答案取 `edges` 中最后出现的。

## A
**一句话。** 并查集按顺序加边，第一条两端已连通的边就是闭合环的那条。

```python
def find_redundant_connection(edges):
    p = list(range(len(edges) + 1))   # 编号 1..n
    def find(x):
        while p[x] != x:
            p[x] = p[p[x]]            # 路径折半
            x = p[x]
        return x
    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            return [a, b]
        p[ra] = rb
```

**复杂度。** 时间 `O(n α(n))`，空间 `O(n)`。

**易错点。**
- 数组按 `0..n-1` 建：节点编号是 `1..n`，`[[1,2],[1,3],[2,3]]` 访问下标 `3` 越界；长度要 `n + 1`。
- 返回环里随便一条边：`[[1,2],[2,3],[3,4],[1,4],[1,5]]` 要求 `[1,4]`，不是 `[1,2]`。
- 合并时写 `p[a] = b` 而不是根：连通块被拆散，判断出错。

**追问。**
- 有向图版本（LC 685）？：还要处理入度为 `2` 的节点，两条候选边分别试。
- 能用 DFS 吗？：每加一条边先 DFS 查两端是否已连通，`O(n^2)`。

**同模式。** LC 261 以图判树、LC 323 无向图中连通分量的数目、LC 685 冗余连接 II、LC 547 省份数量
