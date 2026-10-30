---
id: tlc-maximum-profit-in-job-scheduling-1-signal
node: b.maximum-profit-in-job-scheduling
type: qa
step: 1
---
## Q
**LC 1235 规划兼职工作**｜Hard · CodeTop 国内累计 1 次 · 最近 2026-05-23（国内 CodeTop）

有 `n` 份兼职工作，各有开始时间、结束时间和报酬；时间重叠的不能同时做，但在 `X` 结束的可以立刻接 `X` 开始的。求最大总报酬。`1 <= n <= 5 * 10^4`，`1 <= startTime[i] < endTime[i] <= 10^9`，`1 <= profit[i] <= 10^4`。例：`startTime = [1,2,3,3]`，`endTime = [3,4,5,6]`，`profit = [50,10,40,70]` → `120`。

题面里哪些信号指向哪个模式？从暴力解怎样一步步推到最优解？

## A
**信号 → 模式。**
- 「选一些**互不重叠**的区间，**最大化总权重**」→ 带权区间调度（weighted interval scheduling）：无权重用贪心，有权重必须 **DP**。
- 时间值到 `10^9` → 不能按时间轴开数组，要**排序 + 二分**。
- `n = 5 * 10^4` → 需要 `O(n log n)`；两两比较兼容性的 `O(n^2)` DP 不够。
- 「在 `X` 结束可以立刻接 `X` 开始」→ 区间是半开的，兼容条件是 `end <= start`（含等号），二分要选对 `bisect_right`。

**推导链。**
1. 暴力：每份工作选或不选，`2^n`。
2. 结构：按**结束时间**排序后，与第 `i` 份兼容的前驱恰好是一个前缀 → `dp[i]` 只依赖前缀最优值，转移 `dp[i+1] = max(dp[i], dp[k] + profit_i)`。
3. 浪费：线性扫描找 `k` 使总复杂度回到 `O(n^2)`。
4. 洞察：结束时间有序，找「结束时间 `<= start` 的个数」就是一次二分（`bisect_right(ends, start)`）。
5. 最优：排序 `O(n log n)` + 每份一次二分，总 `O(n log n)`。

**同模式的题**：LC 1751、LC 2008 出租车的最大盈利、LC 435 无重叠区间、LC 646 最长数对链。
