---
slug: same-tree
---
## Q
**LC 100 相同的树**｜Easy

给你两棵二叉树的根节点 `p` 和 `q`，检验这两棵树是否相同：结构上相同，并且对应节点的值相同。两棵树的节点数都在 `[0, 100]`，`-10^4 <= Node.val <= 10^4`。例：`p = [1,2,3], q = [1,2,3]` → `true`；`p = [1,2], q = [1,null,2]` → `false`；`p = [1,2,1], q = [1,1,2]` → `false`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 两棵树同步递归（DFS）：对应位置同时下探，逐点比较。

**一句话。** 两棵树相同，当且仅当两个根都为空，或者根值相等且左子树相同、右子树相同。

**识别。** 「比较两棵树」= 两个指针同时走：空与空相等，空与非空不等，其余比较值再比较子树。`n <= 100`，`O(n)` 足够。

**推导。** 先序列化再比较字符串也行，但要带空节点标记才不会丢结构。同步递归不需要中间产物：按定义分三种情况，其中「恰好一个为空」必须单独判，这一步就是结构比较。

```python
def is_same_tree(p: TreeNode | None, q: TreeNode | None) -> bool:
    if p is None or q is None:
        return p is q                              # 同为空才相同；一空一非空，结构不同
    return (p.val == q.val                         # 值相同
            and is_same_tree(p.left, q.left)       # 左右子树分别相同；and 短路，一处不同就不再往下
            and is_same_tree(p.right, q.right))
```

运行：`[1,2,3]` 与 `[1,2,3]` → `True`；`[1,2]` 与 `[1,null,2]` → `False`；`[1,2,1]` 与 `[1,1,2]` → `False`；`[]` 与 `[]` → `True`；`[]` 与 `[0]` → `False`。

**复杂度。** 时间 `O(min(n, m))`，最多访问较小树的节点数；空间 `O(h)`，递归栈。

**拓展优化。**
- 迭代：栈里放成对的节点，成对弹出比较。
```python
def is_same_tree_iter(p: TreeNode | None, q: TreeNode | None) -> bool:
    stack = [(p, q)]
    while stack:
        a, b = stack.pop()
        if a is None or b is None:
            if a is not b:                         # 一空一非空
                return False
            continue
        if a.val != b.val:
            return False
        stack.append((a.left, b.left))             # 对应位置成对入栈
        stack.append((a.right, b.right))
    return True
```

**易错点。**
- 只比较遍历出来的值序列、不带空节点标记：`[1,2]` 与 `[1,null,2]` 的前序都是 `[1,2]`，会判 `True`，正确是 `False`。
- 只在 `p` 非空时检查 `q`：写成 `if p is None: return q is None` 后直接访问 `q.val`，`p` 非空 `q` 为空时抛 `AttributeError`。一个条件同时处理两个空。
- 递归深度：链状树最多 `n` 层，CPython 默认上限约 `1000`；这里 `n <= 100` 安全。

**同模式。** LC 101 对称二叉树、LC 572 另一棵树的子树、LC 617 合并二叉树、LC 951 翻转等价二叉树。
