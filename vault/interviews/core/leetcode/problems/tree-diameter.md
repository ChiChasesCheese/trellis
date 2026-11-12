---
slug: tree-diameter
---
## Q
**LC 1245 树的直径**｜Medium

给一棵无向树的边列表，求最长简单路径的边数。

## A
**一句话。** 每条路径有个最高点：DFS 取每个节点向下最长的两条分支，两者之和的最大值就是直径。

```python
def tree_diameter(edges):
    g = defaultdict(list)
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)
    ans = 0

    def height(node, parent):    # node 向下最长路径的边数
        nonlocal ans
        top1 = top2 = 0
        for nxt in g[node]:
            if nxt == parent:
                continue
            h = height(nxt, node) + 1
            if h > top1:
                top1, top2 = h, top1
            elif h > top2:
                top2 = h
        ans = max(ans, top1 + top2)   # 以 node 为最高点
        return top1                   # 对父亲只能给一条分支

    height(0, -1)
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 把 `top1 + top2` 返回给父亲：两条分支相加不是向下的路径，父亲再接就拐了回头弯，`[[0,1],[1,2],[1,3]]` 得 `3`，应为 `2`。
- `top1`、`top2` 初值设成负无穷：缺的分支应算 `0`，`[[0,1]]` 会得到负数。
- 链状树深度 `10^4`：递归超过 CPython 默认上限，`RecursionError`。

**追问。**
- 不用递归怎么做？：两次 BFS，从任意点找最远点 `u`，再从 `u` 找最远距离，就是直径（不适用于负权）。
- 要输出直径路径？：BFS 时记前驱，从第二个端点回溯。

**同模式。** LC 543 二叉树的直径、LC 124 二叉树中的最大路径和、LC 687 最长同值路径、LC 310 最小高度树
