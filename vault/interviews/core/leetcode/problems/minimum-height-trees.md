---
slug: minimum-height-trees
---
## Q
**LC 310 最小高度树**｜Medium

给 `n` 个结点的无向树，选任意结点作根使树高最小，返回所有这样的根。

## A
**一句话。** 拓扑剥叶子：反复删掉当前所有叶子，直到剩 `1` 或 `2` 个结点，它们就是树的中心。

```python
def find_min_height_trees(n, edges):
    if n <= 2:
        return list(range(n))
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    leaves = [i for i in range(n) if len(adj[i]) == 1]
    remain = n
    while remain > 2:
        remain -= len(leaves)
        nxt = []
        for leaf in leaves:
            (nb,) = adj[leaf]       # 叶子只有一个邻居
            adj[nb].remove(leaf)
            if len(adj[nb]) == 1:   # 邻居变成新叶子
                nxt.append(nb)
        leaves = nxt
    return leaves
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 对每个结点 BFS 求高度：`O(n²)`，`n=2·10^4` 超时。
- `n=1` 交给通用流程：没有度为 `1` 的结点，返回 `[]`，应为 `[0]`。
- 循环条件写成 `remain > 1`：路径 `0-1-2-3` 会把 `1`、`2` 也剥光。

**追问。**
- 为什么最多两个答案？：树的中心是最长路径（直径）的中点，直径长度奇偶决定一个或两个。
- 还有别的解法吗？：两次 BFS 求直径，取路径中点。

**同模式。** LC 207 课程表、LC 210 课程表 II、LC 543 二叉树的直径、LC 1245 树的直径
