---
id: tlc-odd-even-linked-list-3-why
node: p4.odd-even-linked-list
type: qa
step: 3
---
## Q
**LC 328 奇偶链表**｜正确性

双指针拆链时，为什么循环条件是 `while even and even.next`？把它写成 `while odd and even` 会怎样？循环里每一步保持的不变量是什么？

## A
**不变量。** 每轮开始时：`odd` 是已摘出的奇链的尾，`even` 是偶链的尾，并且 `odd.next` 恰好就是 `even`；`even` 之后才是还没处理的节点；两条链内部保持原顺序。

**为什么是 `even and even.next`。** 一轮要做的事是「取走 `even.next` 这个奇节点」。所以必须保证 `even` 存在、`even.next` 存在。奇数长度时，`even.next` 为空先结束；偶数长度时，`even` 先变成空。循环退出时 `odd` 一定仍是有效节点（它是最后一个奇节点），才能执行 `odd.next = even_head`。

**反例 `[1,2,3,4]`。** 正确答案 `[1,3,2,4]`。
- 写成 `while odd and even`：第一轮后 `odd = 3`、`even = 4`，条件仍成立；
- 第二轮 `odd.next = even.next`（空），`odd = odd.next` 变成 `None`，下一行读 `odd.next` 抛 `AttributeError`；`[1,2]` 同样崩溃。
- 正确条件下第二轮因 `even.next` 为空不进入，`odd` 停在 `3`，接上 `even_head` 得到 `[1,3,2,4]`。
