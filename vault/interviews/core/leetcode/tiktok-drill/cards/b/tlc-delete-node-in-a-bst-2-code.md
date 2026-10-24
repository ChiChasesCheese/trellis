---
id: tlc-delete-node-in-a-bst-2-code
node: b.delete-node-in-a-bst
type: qa
step: 2
---
## Q
**LC 450 删除二叉搜索树中的节点**｜写出 Python 实现

`TreeNode` 有 `val`、`left`、`right`。给定 BST 的根（节点数 `0` 到 `10^4`，值唯一）和 `key`，删除值为 `key` 的节点并保持 BST 性质，返回根；`key` 不存在则不变。要求 `O(h)` 时间，树可能退化成链。

## A
**思路。** 沿 BST 找到目标节点并记住父节点。目标有两个孩子时，找到右子树最左的后继，把后继的值抄到目标上，然后把「要删的节点」换成后继（父节点相应换成后继的父节点）。此时要删的节点至多一个孩子，让孩子顶替它在父节点下的位置；若没有父节点，说明删的是根，直接返回孩子。

```python
def delete_node(root: TreeNode | None, key: int) -> TreeNode | None:
    parent, node = None, root
    while node and node.val != key:            # 先找到 key 所在的节点和它的父节点
        parent = node
        node = node.left if key < node.val else node.right
    if node is None:
        return root                            # 树里没有 key
    if node.left and node.right:               # 两个孩子：用中序后继（右子树最小值）顶替
        succ_parent, succ = node, node.right
        while succ.left:
            succ_parent, succ = succ, succ.left
        node.val = succ.val
        parent, node = succ_parent, succ       # 问题转成删除后继，它至多有一个右孩子
    child = node.left or node.right            # 至多一个孩子：让孩子顶替自己的位置
    if parent is None:
        return child                           # 删的是根
    if parent.left is node:
        parent.left = child
    else:
        parent.right = child
    return root
```

运行：`[5,3,6,2,4,null,7]` 删 `3` → `[5,4,6,2,null,null,7]`；删 `0` → `[5,3,6,2,4,null,7]`；删根 `5` → `[6,3,7,2,4]`；`[]` 删 `0` → `[]`；`[1]` 删 `1` → `[]`；`10^4` 个节点的右斜链删两个节点不抛 `RecursionError`。

**复杂度。** 时间 `O(h)`：向下找目标一条路径，找后继再一条路径；空间 `O(1)`，没有递归。

**写法要点。** `node.left if key < node.val else node.right` 一行决定方向；`child = node.left or node.right` 在「至多一个孩子」时取到那个孩子或 `None`；用 `parent.left is node`（身份比较）判断挂在哪一侧，不依赖值，后继的父节点就是目标时也自然成立；`succ_parent, succ = succ, succ.left` 元组赋值同时前进两个指针。
