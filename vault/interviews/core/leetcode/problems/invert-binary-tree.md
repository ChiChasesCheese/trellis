---
slug: invert-binary-tree
---
## Q
**LC 226 翻转二叉树**｜Easy

翻转二叉树：每个节点的左右子树互换，返回根节点。

## A
**一句话。** 递归翻转左右子树，再让当前节点的左右指针互换。

```python
def invert_tree(root):
    if not root:
        return None
    l, r = invert_tree(root.left), invert_tree(root.right)
    root.left, root.right = r, l
    return root
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- 分两行赋值：第二行用到的 `root.left` 已被覆盖，两边变成同一棵子树，`[2,1,3]` 得 `[2,3,3]`。
- 只交换根的两个孩子、不递归：下面几层没翻。

**追问。**
- 不用递归怎么写？：BFS 或显式栈，弹出节点就交换它的两个孩子再入队。
- 为什么先序、后序都行？：交换与子树内部的翻转互不影响，只要每个节点交换一次。

**同模式。** LC 101 对称二叉树、LC 100 相同的树、LC 617 合并二叉树、LC 104 二叉树的最大深度
