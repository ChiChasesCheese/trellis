---
slug: construct-binary-tree-from-preorder-and-inorder-traversal
---
## Q
**LC 105 从前序与中序遍历序列构造二叉树**｜Medium

给无重复元素的二叉树前序和中序遍历，构造这棵树。

## A
**一句话。** 前序的下一个元素就是根，它在中序里的位置把中序切成左右子树，前序顺序消费，先左后右。

```python
def build_tree(preorder, inorder):
    pos = {v: i for i, v in enumerate(inorder)}  # 值 -> 中序下标
    pre = iter(preorder)         # 按 根、左、右 依次消费
    def build(lo, hi):           # 当前子树对应 inorder[lo:hi]
        if lo >= hi:
            return None
        val = next(pre)
        mid = pos[val]
        node = TreeNode(val)
        node.left = build(lo, mid)     # 必须先左后右
        node.right = build(mid + 1, hi)
        return node
    return build(0, len(inorder))
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 先建右再建左：前序里左子树在前，值被分错，很快 `StopIteration`。
- 每层 `inorder.index` 加切片：每层 `O(n)`，总 `O(n^2)`。

**追问。**
- 只给前序和后序行吗？：一般不行，只有一个孩子时分不清左右（LC 889 接受任意一种）。
- 有重复值怎么办？：哈希表无法唯一定位根，树也可能不唯一，需要额外信息。

**同模式。** LC 106 从中序与后序遍历序列构造二叉树、LC 889 从前序与后序遍历序列构造二叉树、LC 108 将有序数组转换为二叉搜索树、LC 297 二叉树的序列化与反序列化
