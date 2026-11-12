---
slug: construct-binary-tree-from-preorder-and-postorder-traversal
---
## Q
**LC 889 从前序与后序遍历序列构造二叉树**｜Medium

给出无重复值二叉树的前序与后序遍历，重构这棵树，多个答案返回任意一个。

## A
**一句话。** 前序第二个元素是左子树根，它在后序中的位置决定左子树大小，据此把两个序列各切成左右两段递归。

```python
def constructFromPrePost(preorder, postorder):
    pos = {v: i for i, v in enumerate(postorder)}

    def build(pre, post, size):   # 两段的起点和结点数
        if size == 0:
            return None
        root = TreeNode(preorder[pre])
        if size == 1:
            return root
        k = pos[preorder[pre + 1]] - post + 1   # 左子树大小
        root.left = build(pre + 1, post, k)
        root.right = build(pre + 1 + k, post + k,
                           size - 1 - k)
        return root

    return build(0, 0, len(preorder))
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 左子树大小漏掉 `+ 1`：下标偏移不是个数，构出的树后序对不上。
- `size == 1` 不单独返回：`preorder[pre + 1]` 越界或读到右兄弟。

**追问。**
- 为什么不能唯一确定？：只有单孩子的结点有左右歧义，合法的树有 `2^k` 棵。
- 前序+中序或中序+后序？：切分依据换成中序里根的位置，同样用「值到下标」字典。

**同模式。** LC 105 前序与中序构造二叉树、LC 106 中序与后序构造二叉树、LC 1008 前序遍历构造二叉搜索树、LC 297 二叉树的序列化与反序列化
