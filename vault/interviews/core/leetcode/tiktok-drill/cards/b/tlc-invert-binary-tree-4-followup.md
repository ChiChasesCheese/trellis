---
id: tlc-invert-binary-tree-4-followup
node: b.invert-binary-tree
type: qa
step: 4
---
## Q
**LC 226 翻转二叉树**｜追问

面试官接着问：（1）不用递归怎么写？（2）树很深（比如 `10^5` 层的链）怎么办？（3）怎样判断一棵树本身是不是轴对称的（LC 101）？

## A
1. **迭代**：用显式栈（或队列），弹出节点后交换左右，再把两个孩子压回去。每个节点处理一次，顺序无关。

```python
def invert_tree_iter(root: TreeNode | None) -> TreeNode | None:
    stack = [root]
    while stack:
        node = stack.pop()
        if node is None:
            continue
        node.left, node.right = node.right, node.left
        stack.append(node.left)
        stack.append(node.right)
    return root
```

`[4,2,7,1,3,6,9]` → `[4,7,2,9,6,3,1]`，`[2,1,3]` → `[2,3,1]`。
2. **很深的树**：递归深度等于树高，CPython 默认上限 `1000`，所以深链要用上面的迭代版；栈只存「还没处理的节点」，内存 `O(n)` 以内。
3. **轴对称**：不改树，只比较。同时走左右两棵子树 `(a, b)`：都空为真，一空一不空为假，否则要求 `a.val == b.val` 且 `(a.left, b.right)`、`(a.right, b.left)` 都对称。可以用栈存放成对的节点，仍是 `O(n)`。

**Python 提醒**：元组赋值 `x, y = y, x` 能安全交换；但 `a.left, a.right = f(a.right), f(a.left)` 里的 `f` 如果会修改 `a`，右边求值顺序（从左到右）就会影响结果，递归函数只修改子树时才安全。
