---
slug: merge-two-binary-trees
---
## Q
**LC 617 合并二叉树**｜Easy

把两棵二叉树叠在一起，重叠节点值相加，只在一棵里的节点原样保留，返回合并后的树。

## A
**一句话。** 同步递归，一边为空就返回另一边，否则值相加再合并左右孩子。

```python
def merge_trees(root1, root2):
    if root1 is None:       # 另一边整棵子树原样保留
        return root2
    if root2 is None:
        return root1
    root1.val += root2.val
    root1.left = merge_trees(root1.left, root2.left)
    root1.right = merge_trees(root1.right, root2.right)
    return root1
```

**复杂度。** 时间 `O(min(n1, n2))`，空间 `O(h)`。

**易错点。**
- 一边为空时返回 `None` 而不是另一边：丢掉独有的子树，`[1]` 与 `[1,2]` 得 `[2]`，应为 `[2,2]`。
- 根节点没先判空：`root1` 为 `None` 时 `root1.val` 抛 `AttributeError`。

**追问。**
- 不许修改输入？：新建节点 `TreeNode(a.val + b.val)`，缺失一侧当作空。
- 树很深怎么办？：显式栈存一对对应节点，一边缺孩子就直接挂另一边。

**同模式。** LC 100 相同的树、LC 101 对称二叉树、LC 226 翻转二叉树、LC 572 另一棵树的子树
