---
slug: symmetric-tree
---
## Q
**LC 101 对称二叉树**｜Easy

判断二叉树是否轴对称（左右两半互为镜像）。

## A
**一句话。** 用栈存放「应当互为镜像的一对子树」，每次配外侧 `(a.left, b.right)` 与内侧 `(a.right, b.left)`。

```python
def is_symmetric(root):
    stack = [(root.left, root.right)]
    while stack:
        a, b = stack.pop()
        if not a and not b:
            continue
        if not a or not b or a.val != b.val:
            return False
        stack.append((a.left, b.right))    # 外侧配外侧
        stack.append((a.right, b.left))    # 内侧配内侧
    return True
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- 同侧配对 `(a.left, b.left)`：`[1,2,2,3,4,4,3]` 被判 `False`，`[1,2,2,null,3,null,3]` 被判 `True`。
- 不压入 `None` 孩子：一边有孩子、另一边没有时就查不出来。

**追问。**
- 递归怎么写？：`mirror(a, b)`：先 `if not a or not b: return a is b`，再比较值并递归 `(a.left, b.right)`、`(a.right, b.left)`。
- 改成 BFS？：用队列成对取出，逻辑完全相同。

**同模式。** LC 100 相同的树、LC 226 翻转二叉树、LC 572 另一棵树的子树、LC 951 翻转等价二叉树
