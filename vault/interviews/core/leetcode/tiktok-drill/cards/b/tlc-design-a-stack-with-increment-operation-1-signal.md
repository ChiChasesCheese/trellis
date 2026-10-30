---
id: tlc-design-a-stack-with-increment-operation-1-signal
node: b.design-a-stack-with-increment-operation
type: qa
step: 1
---
## Q
**LC 1381 设计一个支持增量操作的栈**｜Medium · CodeTop 国内累计 2 次 · 最近 2026-04-10（国内 CodeTop）

实现 `CustomStack`：`CustomStack(maxSize)` 设定栈的容量；`push(x)`：栈未满时把 `x` 压到栈顶，满了就忽略；`pop()`：弹出并返回栈顶，栈空返回 `-1`；`increment(k, val)`：**栈底**的 `k` 个元素都加 `val`，元素不足 `k` 个时全部加 `val`。`1 <= maxSize, x, k <= 1000`，`0 <= val <= 100`，三种操作各最多调用 `1000` 次。例：容量 3，`push(1)`、`push(2)`、`pop()` → `2`，`push(2)`、`push(3)`、`push(4)`（已满，忽略），`increment(5, 100)`、`increment(2, 100)`，之后四次 `pop()` → `103`、`202`、`201`、`-1`。

题面里哪些信号指向哪个模式？从暴力解怎样一步步推到最优解？

## A
**信号 → 模式。**
- `increment` 修改「栈底 `k` 个」是一段**前缀区间**更新，而读取只在**栈顶**发生 → **懒标记**：先记账，读到时再结算。
- 区间更新只在边界记一笔 → **差分数组**（difference array）的思想，按从栈顶往下的方向累加。
- 约束 `1000` 次操作 → `O(k)` 直接循环也能过，但面试要 `O(1)`。

**推导链。**
1. 直接：`increment` 循环逐个加，`O(k)`，`push`、`pop` 是 `O(1)`。
2. 浪费：栈底元素要很久才被读取，提前加纯属多余。
3. 关键：「下标 `0..k-1` 都加 `val`」只记在 `add[k-1]`；某格成为栈顶被弹出时，它的欠账就是 `add[i]`，再把它传给 `add[i-1]`。
4. 最优：三种操作都是 `O(1)`，额外空间 `O(maxSize)`。

**同模式的题**：LC 370 区间加法、LC 1109 航班预订统计、LC 155 最小栈。
