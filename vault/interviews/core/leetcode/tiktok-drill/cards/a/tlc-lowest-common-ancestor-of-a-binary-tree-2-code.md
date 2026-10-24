---
id: tlc-lowest-common-ancestor-of-a-binary-tree-2-code
node: a.lowest-common-ancestor-of-a-binary-tree
type: qa
step: 2
---
## Q
**LC 236 二叉树的最近公共祖先**｜写出 Python 实现

二叉树根节点 `root`，节点数 `[2, 10^5]`，节点值互不相同，`p != q` 且都在树中。返回 `p`、`q` 的最近公共祖先节点（节点可以是自己的祖先）。树可能是 `10^5` 层的单链，要求不触发递归上限。

## A
**思路。** 用显式栈遍历整棵树，给每个节点记下父节点，`p`、`q` 都有了父指针就停。然后把 `p` 本身和它的全部祖先放进集合，让 `q` 沿父指针向上爬，第一个落进集合的节点就是最近公共祖先。

```python
def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
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

运行：`[3,5,1,6,2,0,8,null,null,7,4]` 中 `p = 5, q = 1` → `3`，`p = 5, q = 4` → `5`；`[1,2]` 中 `p = 1, q = 2` → `1`；`10^5` 个节点的单链树，取最深的两个节点 → 较浅的那个，没有 `RecursionError`。

**复杂度。** 时间 `O(n)`：每个节点最多入栈一次，两条链各走至多 `n` 步；空间 `O(n)`：父指针表、栈和集合。

**写法要点。** 字典 `parent` 的键是节点对象本身：`TreeNode` 没有重写 `__eq__` 和 `__hash__`，默认按身份哈希，正好是我们要的；给字典写类型 `dict[TreeNode, TreeNode | None]`，根的父亲是 `None`；`while p not in parent or q not in parent` 把终止条件写成字典的成员判断；`for child in (node.left, node.right)` 配 `if child` 一行过滤空孩子；用 `set` 做 `O(1)` 的成员测试，比对两条链逐个比较省一层嵌套循环。
