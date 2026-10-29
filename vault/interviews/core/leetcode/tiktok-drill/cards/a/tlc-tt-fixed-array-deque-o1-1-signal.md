---
id: tlc-tt-fixed-array-deque-o1-1-signal
node: a.tt-fixed-array-deque-o1
type: qa
step: 1
---
## Q
**定长数组实现的双端队列（所有操作 O(1)）**｜Medium · 近一年被问：美国 4 次、国内 0 次 · 最近 2026-07-06（面试记录）

用一个定长数组实现双端结构 `FixedDeque(capacity)`，所有操作 `O(1)`：`push_head(x)`、`push_tail(x)`（成功 `True`，已满 `False`）；`pop_head()`、`pop_tail()`（返回值，空时返回 `None`）；`index(i)` 返回从队首数起第 `i` 个元素（`0` 起），越界返回 `None`。类似 Redis 的 `lpush`、`rpush`、`lpop`、`rpop`、`index`。`1 <= capacity <= 10^5`。例：容量 `3`，`push_tail(1)`、`push_head(2)`、`push_tail(3)`，`index(0..2)` → `2, 1, 3`。

题面里哪些信号指向哪个模式？从暴力解怎样一步步推到最优解？

## A
**信号 → 模式。**
- 「定长数组、两端都能进出、都要 `O(1)`」→ 环形缓冲区（ring buffer）：下标对容量取模，数组首尾相接。
- 「按位置访问 `index`」→ 需要随机访问，链表不满足；环形数组的第 `i` 个元素在 `(head + i) % cap`。
- 「满 / 空判定」→ 用元素个数 `size`，不要只靠两个下标（空和满时都相等）。
- 「`search` 是 `O(1)`」→ 多半指按位置访问；按值查找要额外的哈希表（追问）。

**推导链。**
1. 暴力：`list` 头部 `insert(0, x)` 与 `pop(0)` 都是 `O(n)`。
2. 浪费：为了让头部有空位，把全部元素整体搬动。
3. 洞察：不固定“队首在下标 `0`”，用 `head` 记录队首；让下标取模首尾相接，队首入队就是 `head - 1`。
4. 最优：`head` 加 `size` 两个整数，五个操作都是常数次下标运算，`O(1)`；空间 `O(capacity)`。

**同模式的题**：LC 641 设计循环双端队列、LC 622 设计循环队列、LC 1670 设计前中后队列、LC 346 数据流中的移动平均值。
