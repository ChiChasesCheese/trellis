---
id: tlc-sort-list-3-why
node: b.sort-list
type: qa
step: 3
---
## Q
**LC 148 排序链表**｜正确性

链表归并排序为什么要让 `fast` 从 `head.next` 出发？这样保证了什么，递归才一定终止？如果 `fast` 也从 `head` 出发，给出出错的输入和现象。

## A
**不变量。** `sort_list(head)` 返回由 `head` 开头的所有节点排好序后的链表。递归成立需要两个条件：两半都是**非空**的，并且都**严格短于**原链表，这样递归深度有限，最终落到长度 `0` 或 `1` 的基线情况。

**为什么 `fast = head.next`。** 设链表长 `n >= 2`。`fast` 每轮前进两格，`slow` 前进一格；`fast` 从 `head.next` 开始，循环结束时 `slow` 停在第 `ceil(n/2)` 个节点，也就是前半段的末尾。于是前半段长 `ceil(n/2)`，后半段长 `floor(n/2)`，`n >= 2` 时两者都大于 `0` 且都小于 `n`。例如 `n = 2`：前半 `1` 个，后半 `1` 个。

**反例：`fast` 从 `head` 出发。** 输入 `[2,1]`：`slow = fast = head`，进入循环，`slow` 走到第二个节点，`fast` 走到 `None`。此时 `mid = slow.next = None`，并把第二个节点的 `next` 设为 `None`，左半段 `head` 仍是 `[2,1]`，长度没有缩短。`sort_list(head)` 又用同样的输入调用自己，永远不会到达基线，最终抛出 `RecursionError`。让 `fast = head.next`：`slow` 停在第一个节点，左半 `[2]`，右半 `[1]`，合并得到 `[1,2]`。

**反例：不断开。** 如果漏掉 `slow.next = None`，左半段 `head` 仍然连着后半段，`sort_list(head)` 处理的是整条链表，同样永远缩不小。
