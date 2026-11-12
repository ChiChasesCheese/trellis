---
slug: maximum-depth-of-binary-tree
---
## Q
**LC 104 二叉树的最大深度**｜Easy

求二叉树根到最远叶子的节点数。

## A
**一句话。** 深度 = 1 + 左右子树深度的较大者，空树为 `0`。

```python
def max_depth(root):
    if root is None:
        return 0
    l, r = max_depth(root.left), max_depth(root.right)
    return 1 + max(l, r)
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- 漏掉 `1 +`：每层都不加自己，永远返回 `0`。
- 链状树递归过深：`10^4` 个节点会触到 CPython 递归上限，改用 BFS。

**追问。**
- BFS 怎么数层？：每层用 `for _ in range(len(q))` 切开，每层加 `1`，不能每弹一个节点就加。
- 最小深度也这样吗？：不行，缺一侧孩子时不能取 `min`（LC 111）。

**同模式。** LC 111 二叉树的最小深度、LC 110 平衡二叉树、LC 543 二叉树的直径、LC 226 翻转二叉树
