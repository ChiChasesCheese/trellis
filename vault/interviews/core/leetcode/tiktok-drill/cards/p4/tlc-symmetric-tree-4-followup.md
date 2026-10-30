---
id: tlc-symmetric-tree-4-followup
node: p4.symmetric-tree
type: qa
step: 4
---
## Q
**LC 101 对称二叉树**｜追问

面试官接着问：（1）用递归怎么写？栈深度会不会有问题？（2）用队列（BFS）怎么写？（3）判断「一棵树是不是另一棵树的子树」（LC 572）怎么复用这里的思路？

## A
1. **递归**：`mirror(a, b)` 表示两棵子树互为镜像。递归深度等于树高，对称树至多约 500 层，不会超过 Python 默认递归上限 1000；普通的二叉树若要递归遍历，单链树 `n = 1000` 就会触顶。
2. **队列版**：初始放入 `root.left, root.right` 两个节点，每次 `popleft` 两个取成一对，判断规则不变，孩子按 `a.left, b.right, a.right, b.left` 的顺序入队。逻辑与栈版一致，只是遍历顺序是按层。
3. **子树判断（LC 572）**：对 `root` 的每个节点 `t`，用「相同的树」`same(t, sub)` 比较，把 `(a.left, b.right)` 换回 `(a.left, b.left)`。最坏 `O(m * n)`，`m`、`n` 为两棵树的大小。

```python
def is_symmetric_rec(root: TreeNode | None) -> bool:
    def mirror(a: TreeNode | None, b: TreeNode | None) -> bool:
        if not a or not b:
            return a is b               # 都空为真；只有一个空为假
        return a.val == b.val and mirror(a.left, b.right) and mirror(a.right, b.left)

    return mirror(root.left, root.right) if root else True
```

**Python 提醒**：`return a is b` 在 `a`、`b` 恰有一个为 `None` 时是 `False`，都为 `None` 时是 `True`，一行表达了两种情形；别写成 `a == b`，节点类默认的 `==` 也是比较身份，但读者会误以为在比较值。
