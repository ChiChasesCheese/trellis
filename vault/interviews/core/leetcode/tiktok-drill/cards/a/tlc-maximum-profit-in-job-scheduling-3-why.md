---
id: tlc-maximum-profit-in-job-scheduling-3-why
node: a.maximum-profit-in-job-scheduling
type: qa
step: 3
---
## Q
**LC 1235 规划兼职工作**｜正确性

按结束时间排序的 DP 中，为什么对第 `i` 份工作，可接的前驱恰好是排序后的前 `k` 份，而且用 `bisect_right`（不是 `bisect_left`）？给出 `bisect_left` 会出错的输入和两种输出。

## A
**不变量。** `dp[i]` 是只用排序后前 `i` 份工作能得到的最大报酬，且 `dp` 单调不减。

**为什么前驱是前缀。** 排序后 `ends` 非降。与第 `i` 份兼容的条件是对方 `end <= start_i`，满足这个条件的工作在非降序列里必然是一个前缀，个数 `k = bisect_right(ends, start_i)`。这个前缀里任意一组互不重叠的工作都能接在第 `i` 份前面，所以做第 `i` 份的最优值就是 `dp[k] + profit_i`。又因为 `end_i > start_i`，第 `i` 份本身不在前缀里，`k <= i`，转移只用到已算好的 `dp`。

**为什么是 `bisect_right`。** 题面允许在 `X` 结束的工作接在 `X` 开始的工作前面，结束时间**等于**开始时间也算兼容。`bisect_right` 把相等的元素算进前缀，`bisect_left` 不算。

**反例。** 示例 1：`startTime = [1,2,3,3]`，`endTime = [3,4,5,6]`，`profit = [50,10,40,70]`。排序后 `ends = [3,4,5,6]`。第 4 份工作开始于 `3`：`bisect_right` 得 `k = 1`，把 `[1,3]`（报酬 50）算作前驱，得 `50 + 70 = 120`；`bisect_left` 得 `k = 0`，前驱为空，最后输出 `70`。
