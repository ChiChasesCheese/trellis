---
id: tlc-lowest-common-ancestor-of-a-binary-tree-4-followup
node: p2.lowest-common-ancestor-of-a-binary-tree
type: qa
step: 4
---
## Q
**LC 236 二叉树的最近公共祖先**｜追问

面试官接着问：（1）单链树 `10^5` 层，递归会怎样，怎么不递归？（2）同一棵树要回答 `10^5` 次不同的 `(p, q)` 查询怎么办？（3）如果 `p`、`q` 不保证在树中呢？

## A
1. **深树与不递归写法**：递归深度等于树高，`10^5` 层的单链树会超过 CPython 默认递归上限（约 `1000`）而抛 `RecursionError`（也可以 `sys.setrecursionlimit` 调高，但要承担栈溢出的风险）。不递归的做法：用显式栈遍历整棵树给每个节点记下父节点（`p`、`q` 都登记后可提前停），把 `p` 自己和它的全部祖先放进集合，让 `q` 沿父指针向上爬，第一个落进集合的节点就是答案；`O(n)` 时间，`O(n)` 空间。集合必须从 `p` **自己**开始：从 `p` 的父节点开始，`p = 5, q = 4` 会返回 `3`，正确答案是 `5`。
2. **多次查询**：一次遍历预处理每个节点的深度和倍增表 `up[k][v]`（`v` 的第 `2^k` 个祖先）。查询时先把较深的节点提升到同一深度，再从大到小尝试同时上跳，预处理 `O(n log n)`，每次查询 `O(log n)`。查询离线给出时，也可以用 Tarjan 离线算法（并查集）。
3. **不保证存在**（LC 1644）：递归版里 `p`、`q` 的「找到」要单独计数，遍历结束后只有两个都找到才返回结果，否则返回 `None`。

```python
def lca_parent(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    parent: dict[TreeNode, TreeNode | None] = {root: None}
    stack = [root]
    while p not in parent or q not in parent:      # p、q 的父指针都登记好就停
        node = stack.pop()
        for child in (node.left, node.right):
            if child:
                parent[child] = node
                stack.append(child)
    ancestors: set[TreeNode] = set()
    node: TreeNode | None = p
    while node:                                    # p 自己和它的全部祖先
        ancestors.add(node)
        node = parent[node]
    node = q
    while node not in ancestors:                   # q 往上爬，第一个撞上的就是答案
        node = parent[node]
    return node
```

**Python 提醒**：字典和集合的键用节点对象本身，`TreeNode` 默认按身份哈希，正是想要的；`left or right`（递归版）返回第一个为真的对象本身，但如果节点类重写了 `__len__` 或 `__bool__`，这个写法会出错。
