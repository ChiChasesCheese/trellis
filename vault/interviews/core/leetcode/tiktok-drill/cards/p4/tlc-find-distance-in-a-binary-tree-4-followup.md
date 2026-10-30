---
id: tlc-find-distance-in-a-binary-tree-4-followup
node: p4.find-distance-in-a-binary-tree
type: qa
step: 4
---
## Q
**LC 1740 找到二叉树中的距离**｜追问

面试官接着问：（1）树退化成 `10^4` 层的链，递归会超限，怎么改成迭代？（2）要返回具体路径而不是长度？（3）同一棵树要回答很多次 `(p, q)` 查询？（4）树是 `n` 个结点的 N 叉树或只给了边表？

## A
1. **迭代**：用显式栈遍历一次，记下每个结点的父结点、深度和「值 → 结点」；然后两个指针沿父指针上行，每步让深度更大的那个往上走，两者重合在 LCA，走过的步数就是距离。`O(n)` 时间，三个字典 `O(n)` 空间，不受递归上限影响。
```python
def find_distance_iter(root: TreeNode | None, p: int, q: int) -> int:
    parent: dict[TreeNode, TreeNode | None] = {root: None}
    depth: dict[TreeNode, int] = {root: 0}
    by_val: dict[int, TreeNode] = {}
    stack = [root]
    while stack:                       # 迭代遍历：树可能退化成 10^4 层的链，递归会爆栈
        node = stack.pop()
        by_val[node.val] = node
        for child in (node.left, node.right):
            if child:
                parent[child], depth[child] = node, depth[node] + 1
                stack.append(child)
    a, b = by_val[p], by_val[q]
    dist = 0
    while a is not b:                  # 总是让更深的那个往上爬一步，直到在 LCA 相遇
        if depth[a] < depth[b]:
            a, b = b, a
        a = parent[a]
        dist += 1
    return dist
```
`10^4` 个结点的左链上 `p=0, q=9999` → `9999`，`p=5000, q=9999` → `4999`；循环条件必须是 `a is not b`：只比较深度会在同一层的两个不同结点上提前停下（`p=6, q=2` 得到 `0`，正确是 `2`）。
2. **返回路径**：爬升时把 `a` 经过的结点追加到 `left_part`，把 `b` 经过的追加到 `right_part`，相遇后 `left_part + [lca] + right_part[::-1]`。关键是别漏掉相遇点，也别重复。
3. **多次查询**：预处理一次 `parent` / `depth`，再建倍增表 `up[k][v]`（`v` 的第 `2^k` 个祖先），每次查询 `O(log n)`；离线批量查询可用 Tarjan 离线 LCA，近似 `O(n + q)`。
4. **N 叉树 / 边表**：不用区分 `left` / `right`，把边建成邻接表 `defaultdict(list)`，从 `p` 做 BFS 到 `q`，层数即距离，`O(n)`；这个做法对任意无环连通图都成立，是兜底写法。

```python
from collections import defaultdict, deque

def tree_distance(edges: list[tuple[int, int]], p: int, q: int) -> int:
    adj: defaultdict[int, list[int]] = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    dist = {p: 0}
    dq = deque([p])
    while dq:
        u = dq.popleft()
        if u == q:
            return dist[u]
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                dq.append(v)
    return -1
```

**Python 提醒**：`defaultdict` 读不存在的键会**插入**一个空列表；判断存在要用 `in`，别用 `adj[x]` 试探。
