---
id: tlc-convert-binary-search-tree-to-sorted-doubly-linked-list-4-followup
node: b.convert-binary-search-tree-to-sorted-doubly-linked-list
type: qa
step: 4
---
## Q
**LC 426 将二叉搜索树转化为排序的双向链表**｜追问

面试官接着问：（1）不要循环，只要普通的双向链表？（2）能不能做到 `O(1)` 额外空间？（3）反过来，给一个排序链表，转成高度平衡的 BST？

## A
1. **普通双向链表**：去掉最后一行的首尾连线，最小节点的 `left` 和最大节点的 `right` 保持 `None`。其余不变。
2. **`O(1)` 空间**：用 Morris 遍历取代栈：对每个有左子树的节点，临时把左子树最右节点的 `right` 指向当前节点作为「线索」，遍历完左子树沿线索回来再拆除。每条边最多走两次，`O(n)` 时间，`O(1)` 额外空间。这里要同时改写 `right` 指针做链表，会和线索冲突，实现很绕，面试里说清思路和代价即可，主解法的 `O(h)` 栈通常足够。
3. **排序链表转平衡 BST（LC 109）**：用快慢指针找中点当根，递归左半、右半；或先数出长度 `n`，按中序顺序建树，链表指针只前进一次，`O(n)`。

**Python 提醒**：迭代中序里的 `while stack or node:` 不能写成 `while stack and node:`：第一轮栈为空，循环直接退出，什么都不遍历；元组赋值 `a.right, b.left = b, a` 右侧先整体求值再赋给左侧各目标，不会因为顺序出现「先改了 `a` 再读 `a`」的错误。
