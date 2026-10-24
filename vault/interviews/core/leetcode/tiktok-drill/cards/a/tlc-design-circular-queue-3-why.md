---
id: tlc-design-circular-queue-3-why
node: a.design-circular-queue
type: qa
step: 3
---
## Q
**LC 622 设计循环队列**｜正确性

循环队列用定长数组 `buf`、队首下标 `head` 和元素个数 `size` 表示，入队写 `(head + size) % k`。为什么用 `size` 就能区分空和满？只存 `head`、`tail` 两个下标、或者队尾下标不取模，各会错成什么样？

## A
**不变量。** 队列里的元素按顺序占据 `buf[head], buf[(head + 1) % k], ..., buf[(head + size - 1) % k]`，`0 <= size <= k`。`size` 是显式记录的，空与满是两个不同的值（`0` 和 `k`），不会混淆；入队写在这段的下一个位置，出队只移动 `head` 并减小 `size`，其余格子的内容无关紧要。

**反例一：只存 `head`、`tail`。** 入队 `k` 个元素之后 `tail` 绕回到 `head`，此时 `head == tail` 同时是空队列的条件，无法区分。常见补救是满的条件写成 `(tail + 1) % k == head`，牺牲一个格子：容量 `3` 的例子，`enQueue(1)`、`enQueue(2)` 之后 `isFull()` 已经是 `True`，第三次 `enQueue(3)` 返回 `False`，而题目要求 `True`。

**反例二：队尾下标不取模。** `Rear()` 写成 `buf[head + size - 1]`。容量 `3`：入队 `1,2,3`，出队一次，再入队 `4`，此时 `head = 1`、`size = 3`，下标 `3` 超出长度 `3`，`IndexError`；正确下标是 `(1 + 3 - 1) % 3 = 0`，取到刚入队的 `4`。

**反例三：空队列不判断。** `Front()` 直接读 `buf[head]`，空队列会返回数组里的残留值，新建的容量 `3` 队列返回初始的 `0`，正确是 `-1`。
