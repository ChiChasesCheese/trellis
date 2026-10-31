---
id: tlc-remove-duplicates-from-sorted-list-ii-4-followup
node: b.remove-duplicates-from-sorted-list-ii
type: qa
step: 4
---
## Q
**LC 82 删除排序链表中的重复元素 II**｜追问

面试官接着问：（1）链表不是有序的？（2）用递归怎么写？（3）改成删除所有**不**重复的结点，只保留出现过多次的值？

## A
1. **无序**：先遍历一遍 `Counter(node.val ...)`，再用哑结点 + `prev` 扫描，把计数不为 `1` 的结点摘掉，`O(n)` 时间 `O(n)` 空间；若不允许额外空间，先对链表归并排序（`O(n log n)`），再用此处。
2. **递归**：`f(head)`：若 `head` 或 `head.next` 为空，返回 `head`；若 `head.val != head.next.val`，`head.next = f(head.next)` 并返回 `head`；否则跳过所有与 `head.val` 相同的结点，返回 `f(段后第一个结点)`。深度最多 `n`（此处 `≤ 300`，远小于递归上限），简洁但占栈。
3. **只保留重复的**：保留条件取反：`cur` 属于重复段时才保留（保留一个或全部看题意），唯一值整个跳过。仍然是同一套 `prev` / 跳段的框架，只是判断方向相反。

**Python 提醒**：`Counter` 对链表遍历可以写生成器：`def values(node): while node: yield node.val; node = node.next`，再 `Counter(values(head))`，避免先建列表。
