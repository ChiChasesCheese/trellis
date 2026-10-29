---
id: tlc-invert-binary-tree-2-code
node: a.invert-binary-tree
type: qa
step: 2
---
## Q
**LC 226 翻转二叉树**｜写出 Python 实现

二叉树节点数在 `[0, 100]`，节点值在 `[-100, 100]`。原地把整棵树左右翻转并返回根节点，空树返回 `None`，要求 `O(n)`。

## A
**思路。** 递归：空树直接返回；否则先分别翻转右子树和左子树，再把结果交叉赋给 `left` 和 `right`。元组赋值的右边先完整求值，所以不需要临时变量，也不会读到被覆盖的新值。

```python
def invert_tree(root: TreeNode | None) -> TreeNode | None:
    if root is None:
        return None
    # 右边的整个表达式先算完，再同时赋给左右，不需要临时变量
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root
```

运行：`[4,2,7,1,3,6,9]` → `[4,7,2,9,6,3,1]`，`[2,1,3]` → `[2,3,1]`，`[]` → `[]`。

**复杂度。** 时间 `O(n)`；空间 `O(h)`，递归栈深等于树高，`h <= 100`。

**写法要点。** `a, b = f(x), g(y)` 先把右边打包成元组再解包，是 Python 里交换两个值的惯用法；返回 `root` 让调用方可以链式使用；空树的 `if root is None` 同时是递归出口。迭代版用 `stack = [root]`，弹出后 `node.left, node.right = node.right, node.left` 再压入两个孩子，空节点 `continue` 跳过。
