---
id: tlc-flatten-binary-tree-to-linked-list-4-followup
node: b.flatten-binary-tree-to-linked-list
type: qa
step: 4
---
## Q
**LC 114 二叉树展开为链表**｜追问

面试官接着问：（1）进阶要求 `O(1)` 额外空间，怎么做？（2）深度 2000 的链，递归在 Python 里会出什么问题，怎么绕开？（3）要展开成中序顺序（比如二叉搜索树转有序链表）怎么改？

## A
1. **`O(1)` 空间（进阶）**：沿 `right` 向下走，遇到有左子树的 `cur`，找到左子树的最右下节点 `pred`，先把原右子树接到 `pred.right`，再把左子树搬到 `cur.right`、`cur.left` 置空。先序顺序不变，这就是 Morris 遍历的核心操作，没有递归栈。内层找末端的循环每个节点至多经过一次，总时间 `O(n)`。

```python
def flatten_o1(root: TreeNode | None) -> None:
    cur = root
    while cur:
        if cur.left:
            pred = cur.left                # 从左孩子出发，沿右链走到头
            while pred.right:
                pred = pred.right
            pred.right = cur.right         # 先把原右子树接在右链末端
            cur.right = cur.left           # 再把左子树整体搬到右边
            cur.left = None
        cur = cur.right
```

`[1,2,5,3,4,null,6]` → `[1,null,2,null,3,null,4,null,5,null,6]`。顺序不能换：先接右子树，再覆盖 `cur.right`。
2. **递归爆栈**：深度 2000 的左链会让递归版抛 `RecursionError`（默认递归上限约 1000）。可以 `sys.setrecursionlimit`，或者用上面的迭代版；还有一种显式栈（先序）：弹出节点，把上一个先序节点的 `right` 指向它，右孩子先入栈、左孩子后入栈，空间 `O(h)`：

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

另一种递归写法「逆后序」：按「右、左、根」处理，保存已经展开好的链头 `prev`，处理 `node` 时 `node.right = prev; node.left = None; prev = node`，不需要返回尾节点，递归深度同样等于树高。
3. **中序**：BST 转有序链表（LC 426）把「根、左、右」换成「左、根、右」：中序遍历时用 `prev` 把上一个节点的 `right` 指向当前节点；用栈迭代最稳。Morris 中序则需要找左子树的最右节点作为线索，空间 `O(1)`。

**Python 提醒**：这类「原地修改、返回 `None`」的函数，本地调试时要自己沿 `right` 把链走一遍才看得到结果；直接打印根节点只能看到第一个节点。
