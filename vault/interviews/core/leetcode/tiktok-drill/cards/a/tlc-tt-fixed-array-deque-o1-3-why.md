---
id: tlc-tt-fixed-array-deque-o1-3-why
node: a.tt-fixed-array-deque-o1
type: qa
step: 3
---
## Q
**定长数组实现的双端队列（所有操作 O(1)）**｜正确性

环形缓冲区用 `head` 和 `size` 表示双端队列，第 `i` 个元素在 `(head + i) % cap`。为什么这个表示在两端入队出队后仍然正确？队尾下标写成 `(head + size) % cap`、`index` 忘记加 `head`、满时仍写入，各会错成什么样？

## A
**不变量。** 队列里的元素按顺序占据 `buf[head], buf[(head + 1) % cap], ..., buf[(head + size - 1) % cap]`，`0 <= size <= cap`。`push_head` 把 `head` 前移一格后写入，新元素成为第 `0` 个，原来的第 `i` 个变成第 `i + 1` 个，仍满足上面的公式；`pop_head` 让 `head` 后移，每个元素的序号减一；两个队尾操作只改 `size`。因此 `index(i)` 恒为 `buf[(head + i) % cap]`。

**反例一：队尾下标多了一格。** 用 `(head + size) % cap` 当队尾元素的位置（那是下一个空位）。容量 `3`，`push_tail(1)` 后 `pop_tail()` 读到空槽，得到 `None`，正确是 `1`。

**反例二：`index` 忘记加 `head`。** `push_tail(1)`、`push_head(2)` 之后数组是 `[1, None, 2]`（`head = 2`，`size = 2`），`index(0)` 直接读 `buf[0]` 得到 `1`，正确是 `2`。只有从不使用 `push_head` 时，`head` 恒为 `0`，这个错误才不暴露。

**反例三：满时仍写入。** 容量 `3` 存满 `[2, 1, 3]` 后再 `push_head(4)`，不检查 `size == cap` 会把 `head` 回退一格并覆盖队尾的 `3`，`size` 变成 `4` 超过容量，队列内容损坏。

**反例四：空时弹出。** 不检查 `size == 0` 就弹出，会返回数组里残留的值（或 `None` 被当成真实元素），`size` 变成负数，之后所有下标公式失效。
