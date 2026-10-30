---
id: tlc-binary-tree-right-side-view-4-followup
node: p2.binary-tree-right-side-view
type: qa
step: 4
---
## Q
**LC 199 二叉树的右视图**｜追问

面试官接着问：（1）用深度优先（DFS）做，空间能比 BFS 更省吗？（2）改成**左视图**？（3）树非常深（比如一条 10^5 的链），递归会怎样？

## A
1. **DFS，右优先**：先访问右子树、再访问左子树，每个深度**第一次**被访问到的节点就是该深度最右的节点，所以只要 `len(ans) == 深度` 就记录。空间是树高 `O(h)`，对瘦高的树比 BFS 的 `O(w)` 省，对完全二叉树则相反。用显式栈实现：先压左孩子、再压右孩子，右孩子先出栈。
```python
def right_side_view_dfs(root: TreeNode | None) -> list[int]:
    ans: list[int] = []
    stack = [(root, 0)] if root else []
    while stack:
        node, depth = stack.pop()
        if depth == len(ans):                      # 这个深度第一次出现：它就是最右的
            ans.append(node.val)
        if node.left:
            stack.append((node.left, depth + 1))
        if node.right:
            stack.append((node.right, depth + 1))  # 后压入的先弹出，右子树先访问
    return ans
```
2. **左视图**：BFS 版把 `level[-1]` 换成 `level[0]`；DFS 版把压栈顺序对调（先压右、后压左）。`[1,2,3,null,5,null,4]` 的左视图是 `[1, 2, 5]`。
3. **深链**：BFS 和上面的显式栈 DFS 都不递归，`10^5` 节点的链照样通过；递归版本在深度超过约 `1000` 时抛 `RecursionError`，题目规模至多 `100` 个节点，递归没问题，但面试里最好说出这个限制。

**Python 提醒**：列表推导里 `if kid` 用对象的真值判断非空，`TreeNode` 没有定义 `__bool__` 或 `__len__` 时一律为真，所以等价于 `kid is not None`；一旦给节点类加了 `__len__`，这种写法会悄悄出错，要显式写 `is not None`。
