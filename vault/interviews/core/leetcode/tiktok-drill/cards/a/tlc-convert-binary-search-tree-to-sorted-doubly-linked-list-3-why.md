---
id: tlc-convert-binary-search-tree-to-sorted-doubly-linked-list-3-why
node: a.convert-binary-search-tree-to-sorted-doubly-linked-list
type: qa
step: 3
---
## Q
**LC 426 将二叉搜索树转化为排序的双向链表**｜正确性

为什么在中序遍历的过程中就能直接改指针，而不会破坏还没走完的部分？遗漏最后的首尾连线或用递归实现，会出什么错？

## A
**不变量。** 每次循环开始（访问 `node` 之前），已经访问的节点 `prev` 及它之前的所有节点已经被串成一条升序的双向链，`prev` 是链尾；栈里和 `node` 子树里的节点还保持原来的树形。

**为什么改指针安全。**
- `node.left`：`node` 被弹出时，它的左子树已全部访问完，不再需要这个指针，可以改成 `prev`。
- `prev.right`：`prev` 的右子树已在上一轮通过 `node = node.right` 取走，进入了当前这一轮的遍历，不再需要原来的 `prev.right`，可以改成当前节点。
- `node.right` 在本轮结尾才读取，此时没被改过，右子树完整。

**反例一：漏掉首尾连线。** `[2,1,3]` 转换后只有 `1 ⇄ 2 ⇄ 3`。沿后继走到 `3` 之后 `3.right` 为 `None`，没有回到 `1`；从 `1` 沿前驱走，`1.left` 是 `None`，期望的 `1,3,2` 得不到。补上 `first.left, prev.right = prev, first` 后，两个方向都是长度 `3` 的环。

**反例二：递归。** 树退化成 `2000` 个节点的右斜链（合法的 BST，每个节点只有右孩子）。递归中序的深度是 `2000`，超过 Python 默认的递归上限 `1000`，抛 `RecursionError`；迭代版把「调用栈」换成显式栈，不受限制，答案正确（最小节点的前驱值是 `1999`）。

**单节点情形。** 只有一个节点时 `first` 和 `prev` 是同一个节点，最后一行让它的 `left` 和 `right` 都指向自己，满足「首尾相连」。
