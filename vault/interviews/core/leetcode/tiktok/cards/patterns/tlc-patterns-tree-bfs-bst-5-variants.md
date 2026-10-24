---
id: tlc-patterns-tree-bfs-bst-5-variants
node: patterns.tree-bfs-bst
type: qa
step: 5
---
## Q
**二叉树 BFS 与 BST 性质｜变形：最大宽度、删除 BST 节点、第 k 小、距离 K**

这几道题在基本模板上各改了哪一步？

## A
**LC 662 最大宽度**：层内节点按完全二叉树**编号**（左孩子 `2i`，右孩子 `2i+1`），一层的宽度 = 最右编号 − 最左编号 + 1。每层减去最左编号避免数字无限增长（Python 整数不溢出，但数字会变慢）。

```python
def width_of_binary_tree(root: TreeNode | None) -> int:
    if not root:
        return 0
    best = 0
    level = [(root, 0)]                    # (节点, 编号)
    while level:
        best = max(best, level[-1][1] - level[0][1] + 1)
        base = level[0][1]
        nxt = []
        for node, idx in level:
            idx -= base
            if node.left:
                nxt.append((node.left, 2 * idx))
            if node.right:
                nxt.append((node.right, 2 * idx + 1))
        level = nxt
    return best
```

`[1,3,2,5,3,null,9]` → `4`；`[1,3,2,5,null,null,9,6,null,7]` → `7`；`[1,3,2,5]` → `2`。

**LC 450 删除 BST 节点**：找到后分三种情况：没有左孩子 → 右孩子顶上；没有右孩子 → 左孩子顶上；两个都有 → 用右子树的最小值（后继）替换当前节点的值，再到右子树里删除后继。

```python
def delete_node(root: TreeNode | None, key: int) -> TreeNode | None:
    if root is None:
        return None
    if key < root.val:
        root.left = delete_node(root.left, key)
    elif key > root.val:
        root.right = delete_node(root.right, key)
    else:
        if root.left is None:
            return root.right
        if root.right is None:
            return root.left
        succ = root.right
        while succ.left:
            succ = succ.left
        root.val = succ.val
        root.right = delete_node(root.right, succ.val)
    return root
```

删除 `[5,3,6,2,4,null,7]` 中的 `3` → 层序 `[5,4,6,2,null,null,7]`。

**LC 230 第 k 小**：迭代中序，数到第 `k` 个就返回，提前停止。**LC 863 距离 K**：先 DFS 给每个节点记父节点，再从目标做 BFS（邻居 = 左、右、父），第 `k` 层的节点即答案；`[3,5,1,6,2,0,8,null,null,7,4]`，目标 `5`，`k=2` → `[7,4,1]`（顺序不限）。
