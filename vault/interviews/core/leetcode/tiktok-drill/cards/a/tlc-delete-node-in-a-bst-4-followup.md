---
id: tlc-delete-node-in-a-bst-4-followup
node: a.delete-node-in-a-bst
type: qa
step: 4
---
## Q
**LC 450 删除二叉搜索树中的节点**｜追问

面试官接着问：（1）递归的标准写法是什么，为什么这里可能不用？（2）用前驱（左子树最大）顶替行不行？（3）节点里存的是很大的对象，不能复制值，只能改指针？

## A
1. **递归写法**（面试里最常见，短）：
```python
def delete_node_rec(root: TreeNode | None, key: int) -> TreeNode | None:
    if root is None:
        return None
    if key < root.val:
        root.left = delete_node_rec(root.left, key)
    elif key > root.val:
        root.right = delete_node_rec(root.right, key)
    else:
        if root.left is None:
            return root.right
        if root.right is None:
            return root.left
        succ = root.right
        while succ.left:
            succ = succ.left
        root.val = succ.val
        root.right = delete_node_rec(root.right, succ.val)
    return root
```
结果与迭代版一致。每层递归返回「删除后的子树根」，父节点用返回值重新接上。树退化成 `10^4` 层的链时，会触发 `RecursionError`，所以面试里写完要说明这个风险。
2. **用前驱**：把右子树换成左子树，找左子树最右的节点，同样正确；删除后树的形状不同，两种结果都是合法答案（示例给出了两个）。
3. **只改指针**：不复制 `succ.val`，而是把 `succ` 节点本身摘下来放到目标位置：先让 `succ_parent` 接管 `succ.right`，再令 `succ.left = node.left`、`succ.right = node.right`（目标的右孩子就是后继时要避免自环），最后让目标的父节点指向 `succ`。

**Python 提醒**：`child = node.left or node.right` 依赖节点对象的真值总是 `True`；如果自定义了 `__len__` 或 `__bool__`，对象可能被当成假值，应改写成 `node.left if node.left is not None else node.right`。
