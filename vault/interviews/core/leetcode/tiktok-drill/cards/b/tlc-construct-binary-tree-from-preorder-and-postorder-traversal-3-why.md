---
id: tlc-construct-binary-tree-from-preorder-and-postorder-traversal-3-why
node: b.construct-binary-tree-from-preorder-and-postorder-traversal
type: qa
step: 3
---
## Q
**LC 889 从前序与后序遍历序列构造二叉树**｜正确性

为什么左子树大小是 `post_idx[left_root] - post_lo + 1`？漏掉 `+ 1` 会得到什么？为什么答案可以不唯一？

## A
**不变量。** 递归调用 `build(pre_lo, post_lo, size)` 时，前序里的 `preorder[pre_lo : pre_lo + size]` 与后序里的 `postorder[post_lo : post_lo + size]` 是同一棵子树的两种遍历。

**左子树大小。** 前序是「根、左子树、右子树」，所以 `preorder[pre_lo + 1]` 是左子树的根；后序是「左子树、右子树、根」，左子树根是左子树后序的**最后一个**元素。于是左子树在后序里占 `post_lo … post_idx[左根]`，共 `post_idx[左根] - post_lo + 1` 个。

**反例（漏掉 `+ 1`）。** 示例 `preorder = [1,2,4,5,3,6,7]`，`postorder = [4,5,2,6,7,3,1]`：根的左根是 `2`，`post_idx[2] = 2`，左子树应有 `3` 个结点（`2,4,5`）。
- 漏掉 `+ 1` 得到 `2`：左子树少了 `5`，构出的树后序是 `[4,2,6,7,3,5,1]`，与输入不符。
- 加上 `+ 1` 得到 `3`，后序 `[4,5,2,6,7,3,1]` 与输入一致。

**为什么不唯一。** 结点只有一个孩子时，前序和后序都分不出它是左还是右。例如 `preorder = [1,2]`、`postorder = [2,1]`：`[1,2]`（2 是左孩子）与 `[1,null,2]`（2 是右孩子）都合法。代码约定 `size > 1` 时前序第二个元素是左根，得到的是其中一种。
