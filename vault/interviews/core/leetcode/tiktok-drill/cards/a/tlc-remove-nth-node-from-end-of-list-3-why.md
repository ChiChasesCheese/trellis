---
id: tlc-remove-nth-node-from-end-of-list-3-why
node: a.remove-nth-node-from-end-of-list
type: qa
step: 3
---
## Q
**LC 19 删除链表的倒数第 N 个节点**｜正确性

快指针先走 `n` 步、再同速前进，为什么到 `fast.next` 为空时 `slow` 恰好停在待删结点的前一个？不用哑结点会在什么输入上出错？

## A
**不变量。** 任何时刻 `fast` 都比 `slow` 前进了恰好 `n` 个结点（沿链表向后数 `n` 步）。

**为什么停在前驱。** 设链表有 `L` 个结点，哑结点编号 `0`，真实结点编号 `1` 到 `L`。
- `fast` 先走 `n` 步，位置是 `n`；之后和 `slow`（位置 `0`）同速走。
- `fast.next` 为空时 `fast` 在位置 `L`，所以 `slow` 在位置 `L - n`。
- 倒数第 `n` 个结点的编号是 `L - n + 1`，`slow` 恰好是它的前驱，`slow.next = slow.next.next` 删除的就是它。

**反例：没有哑结点。** 直接从 `head` 出发（`fast = slow = head`），先走 `n` 步，再 `while fast.next`：
- 输入 `[1]`、`n = 1`：`fast` 走一步变成 `None`，随后访问 `fast.next`，抛 `AttributeError: 'NoneType' object has no attribute 'next'`。
- 输入 `[1,2]`、`n = 2`（删头）：同理，`fast` 走完 `n` 步已经是 `None`。

删头结点时，它没有前驱可供 `slow` 指向，而且 `fast` 会走出链尾。有哑结点时，`fast` 从位置 `0` 走 `n` 步最远到位置 `L`，不会越过链尾；`slow` 停在哑结点上也能完成删除：`[1]`、`n = 1` 得到 `[]`，`[1,2]`、`n = 2` 得到 `[2]`。
