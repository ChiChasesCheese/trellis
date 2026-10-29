---
id: tlc-flatten-binary-tree-to-linked-list-4-followup
node: a.flatten-binary-tree-to-linked-list
type: qa
step: 4
---
## Q
**LC 114 二叉树展开为链表**｜追问

面试官接着问：（1）不要求 `O(1)` 空间时，最直观的迭代写法是什么？（2）为什么递归「逆后序」写法能工作，有什么风险？（3）要展开成中序顺序（比如二叉搜索树转有序链表）怎么改？

## A
1. **显式栈（先序）**：弹出节点，把上一个先序节点的 `right` 指向它；右孩子先入栈、左孩子后入栈，保证左子树先出栈。空间 `O(h)`。

```python
def flatten_stack(root: TreeNode | None) -> None:
    if root is None:
        return
    stack = [root]
    prev: TreeNode | None = None
    while stack:
        node = stack.pop()
        if prev:
            prev.left, prev.right = None, node     # 上一个先序节点的右指针指向当前节点
        if node.right:
            stack.append(node.right)               # 右先入栈，左后入栈，左先出
        if node.left:
            stack.append(node.left)
        prev = node
```

`[1,2,5,3,4,null,6]` → `[1,null,2,null,3,null,4,null,5,null,6]`。
2. **逆后序递归**：按「右、左、根」的顺序处理，保存已经展开好的链头 `prev`，处理 `node` 时 `node.right = prev; node.left = None; prev = node`。因为先处理的是先序里靠后的节点，拼接方向是从后往前，不需要找最右下节点。风险：递归深度等于树高，深度 2000 的树在 Python 里会 `RecursionError`。
3. **中序**：BST 转有序链表（LC 426）把「根、左、右」换成「左、根、右」：中序遍历时用 `prev` 把上一个节点的 `right` 指向当前节点；用栈迭代最稳。Morris 中序则需要找左子树的最右节点作为线索，空间 `O(1)`。

**Python 提醒**：这类「原地修改、返回 `None`」的函数，本地调试时要自己沿 `right` 把链走一遍才看得到结果；直接打印根节点只能看到第一个节点。
