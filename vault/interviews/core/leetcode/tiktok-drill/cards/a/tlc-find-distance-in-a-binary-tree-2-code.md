---
id: tlc-find-distance-in-a-binary-tree-2-code
node: a.find-distance-in-a-binary-tree
type: qa
step: 2
---
## Q
**LC 1740 找到二叉树中的距离**｜写出 Python 实现

二叉树（结点数 `[1, 10^4]`，值唯一，`0 <= Node.val <= 10^9`）与两个存在于树中的值 `p`、`q`，返回二者之间路径的边数。要求能处理 `10^4` 层的单链。

## A
**思路。** 迭代遍历一次，记下每个结点的父结点、深度，以及「值 → 结点」；然后两个指针沿父指针上行：每步让深度更大的那个往上走，两者重合在 LCA，走过的步数就是距离。

```python
def find_distance(root: TreeNode | None, p: int, q: int) -> int:
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

运行：示例树上 `p=5, q=0` → `3`，`p=5, q=7` → `2`，`p=5, q=5` → `0`；单结点树 `p=q=7` → `0`；`10^4` 个结点的左链上 `p=0, q=9999` → `9999`，`p=5000, q=9999` → `4999`。

**复杂度。** 时间 `O(n)`：遍历一次加最多 `O(n)` 步上行；空间 `O(n)`：三个字典与栈。

**写法要点。** 用显式栈代替递归，避开 `RecursionError`；`TreeNode` 默认按对象身份哈希，可直接作字典键；`parent[child], depth[child] = node, depth[node] + 1` 一行同时登记两个表；`a, b = b, a` 交换让「更深者」始终是 `a`，循环体只写一个分支；`a is not b` 比较对象身份，不比较值。
