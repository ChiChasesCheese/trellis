---
id: tlc-delete-node-in-a-bst-4-followup
node: p4.delete-node-in-a-bst
type: qa
step: 4
---
## Q
**LC 450 删除二叉搜索树中的节点**｜追问

面试官接着问：（1）树退化成 `10^4` 层的链，递归会超限，怎么改成迭代？（2）用前驱（左子树最大）顶替行不行？（3）节点里存的是很大的对象，不能复制值，只能改指针？

## A
1. **迭代写法**（`O(1)` 额外空间，不受递归上限影响）：先沿路径找到目标和它的父节点；两个孩子时找到后继，把后继的值抄上来，然后把「要删的节点」换成后继；此时至多一个孩子，让孩子顶替它在父节点下的位置，没有父节点就是删根。
```python
def delete_node_iter(root: TreeNode | None, key: int) -> TreeNode | None:
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
结果与递归版一致，`10^4` 层的右斜链上删 `5000` 也不抛 `RecursionError`。用 `parent.left is node` 判断挂在哪一侧，后继的父节点就是目标本身时也成立。
2. **用前驱**：把右子树换成左子树，找左子树最右的节点，同样正确；删除后树的形状不同，两种结果都是合法答案（示例给出了两个）。
3. **只改指针**：不复制 `succ.val`，而是把 `succ` 节点本身摘下来放到目标位置：先让 `succ_parent` 接管 `succ.right`，再令 `succ.left = node.left`、`succ.right = node.right`（目标的右孩子就是后继时要避免自环），最后让目标的父节点指向 `succ`。

**Python 提醒**：`child = node.left or node.right` 依赖节点对象的真值总是 `True`；如果自定义了 `__len__` 或 `__bool__`，对象可能被当成假值，应改写成 `node.left if node.left is not None else node.right`。
