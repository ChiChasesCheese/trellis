---
id: tlc-symmetric-tree-2-code
node: p4.symmetric-tree
type: qa
step: 2
---
## Q
**LC 101 对称二叉树**｜写出 Python 实现

二叉树根节点 `root`，节点数 `[1, 1000]`，节点值 `-100 <= Node.val <= 100`。判断它是否轴对称，用迭代实现。

## A
**思路。** 栈里存放「应当互为镜像的一对子树」，初始是根的左右孩子。弹出一对 `(a, b)`：两个都空，这一对没问题；只有一个空，或者值不同，直接返回 `False`；否则要求外侧 `(a.left, b.right)` 和内侧 `(a.right, b.left)` 也互为镜像，把这两对压栈。栈空了仍没有失败，就是对称的。

```python
def is_symmetric(root: TreeNode | None) -> bool:
    if root is None:
        return True
    stack = [(root.left, root.right)]   # 每一对是应当互为镜像的两棵子树
    while stack:
        a, b = stack.pop()
        if a is None and b is None:
            continue
        if a is None or b is None or a.val != b.val:
            return False
        stack.append((a.left, b.right))     # 外侧配外侧
        stack.append((a.right, b.left))     # 内侧配内侧
    return True
```

运行：`[1,2,2,3,4,4,3]` → `True`，`[1,2,2,null,3,null,3]` → `False`，`[1]` → `True`，`[1,1,null,1]` → `False`，左边挂 999 层链、右边为空的树 → `False`。

**复杂度。** 时间 `O(n)`：每个节点至多出现在一对里一次；空间 `O(h)`，`h` 为树高。

**写法要点。** 栈里直接放元组 `(a, b)`，弹出时用解包 `a, b = stack.pop()`；判空用 `is None` 而不是 `not a`，对节点对象两者等价，但 `is None` 更明确地表示「没有这个孩子」；`a is None or b is None or a.val != b.val` 靠短路求值，保证访问 `.val` 时两边都非空；两处 `append` 的顺序不影响结果，因为要检查的是全部配对。
