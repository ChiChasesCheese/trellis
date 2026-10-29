---
id: tlc-lowest-common-ancestor-of-a-binary-search-tree-3-why
node: b.lowest-common-ancestor-of-a-binary-search-tree
type: qa
step: 3
---
## Q
**LC 235 二叉搜索树的最近公共祖先**｜Easy · 字节高频｜正确性

为什么「第一个值落在 `[min(p, q), max(p, q)]` 里的结点」就是 LCA？这个区间为什么必须是闭区间？写成严格不等号会在什么输入上出错？

## A
**不变量。** 循环中的 `node` 始终是 `p` 和 `q` 的公共祖先（初始是根，必然成立）。
- `node.val < lo`：`p`、`q` 的值都大于 `node.val`，按 BST 的性质二者都在右子树，右孩子仍是公共祖先，下降不破坏不变量。
- `node.val > hi`：同理走左。
- 其余 `lo <= node.val <= hi`：若 `lo < node.val < hi`，二者分居左右，任何孩子都至多包含其一，`node` 是最深的公共祖先；若 `node.val` 等于其中一个，该结点就是 `p`（或 `q`）本身，另一个在它的子树里，它自己是自己的祖先，也是最深的公共祖先。

**反例：严格不等号。** 把停止条件写成 `p.val < node.val < q.val`，在 `root = [6,2,8,0,4,7,9,null,null,3,5]` 上：
- `p = 2, q = 4`：结点 `2` 的值等于 `p.val`，条件为假，继续往下，最后走出树返回 `None`；正确答案是结点 `2`。
- `p = 8, q = 2`（顺序反过来）：区间 `8 < node.val < 2` 永远为假，返回 `None`；正确答案是结点 `6`。
