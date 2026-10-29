---
id: tlc-construct-binary-tree-from-preorder-and-postorder-traversal-4-followup
node: b.construct-binary-tree-from-preorder-and-postorder-traversal
type: qa
step: 4
---
## Q
**LC 889 从前序与后序遍历序列构造二叉树**｜追问

面试官接着问：（1）满足这对遍历序列的树一共有多少棵？（2）改成「前序 + 中序」（LC 105）怎么改？（3）树很深（链状 `10^5`）时递归会爆栈，怎么办？

## A
1. **计数**：只有「恰好一个孩子」的结点有歧义（孩子可以是左或右），其他结点的形状被序列确定。设这样的结点有 `k` 个，合法的树恰好 `2^k` 棵；
2. **前序 + 中序**：根的位置取自中序：`inorder` 里根的下标 `i`，左子树大小 `i - in_lo`，右子树大小 `size - 1 - 左大小`；预建 `值 → 中序下标` 字典。此时答案**唯一**，不需要「单孩子默认左」的约定。
3. **深树**：改成显式栈迭代。思路：按前序顺序逐个建结点，用栈保存「还没封口的祖先」；同时用后序指针 `j`，当栈顶的值等于 `postorder[j]` 时说明该结点的子树已结束，弹栈并 `j += 1`；新结点接到栈顶的 `left`（若为空）或 `right`。每个结点进出栈一次，`O(n)`，不依赖递归深度。

**Python 提醒**：`list.index` 是 `O(n)` 线性查找，放在递归里整体变成 `O(n^2)`；需要「值 → 位置」时一开始就用字典或 `{v: i for i, v in enumerate(a)}` 建好。
