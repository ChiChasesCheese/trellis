---
id: tlc-maximum-profit-in-job-scheduling-0-whole
node: b.maximum-profit-in-job-scheduling
type: qa
---
## Q
**LC 1235 规划兼职工作**｜Hard · CodeTop 国内累计 1 次 · 最近 2026-05-23（国内 CodeTop）

有 `n` 份兼职工作，第 `i` 份从 `startTime[i]` 开始、`endTime[i]` 结束，报酬 `profit[i]`。时间上重叠的两份工作不能同时做；在时间 `X` 结束的工作，可以立刻接在 `X` 开始的下一份。求能获得的最大报酬。`1 <= n <= 5 * 10^4`，`1 <= startTime[i] < endTime[i] <= 10^9`，`1 <= profit[i] <= 10^4`。例：`startTime = [1,2,3,3]`，`endTime = [3,4,5,6]`，`profit = [50,10,40,70]` → `120`（做 `[1,3]` 和 `[3,6]`）；`startTime = [1,1,1]`，`endTime = [2,3,4]`，`profit = [5,6,4]` → `6`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 按**结束时间**排序后做一维 DP：`dp[i]` 是只考虑前 `i` 份工作的最大报酬，做第 `i` 份就接在「结束时间 `<=` 它开始时间」的最后一份之后，用 `bisect_right` 二分找到这个位置，`dp[i+1] = max(dp[i], dp[k] + 报酬)`。`O(n log n)`。

**识别。** 「每份工作选或不选 + 选中的区间互不重叠 + 求最大总权重」是**带权区间调度**（weighted interval scheduling），贪心（按结束时间挑）不适用于有权重的情形，要用 DP；时间到 `10^9` 所以不能按时间轴建数组，只能对工作排序后二分；`n = 5 * 10^4` 要 `O(n log n)`，`O(n^2)` 的两两兼容判断不够。

**推导。** 暴力：每份工作选或不选，`2^n`。结构：按结束时间排序后，选第 `i` 份工作时，前面能接的工作恰好是排序后的一个**前缀**（结束时间 `<=` 它的开始时间），所以子问题只依赖「前缀的最优值」。DP：`dp[i]` 是前 `i` 份的最大报酬，转移 = 不做 `dp[i]` 或做 `dp[k] + profit`。浪费：为找 `k` 线性扫描会让总复杂度变成 `O(n^2)`；结束时间已有序，用二分把找 `k` 降到 `O(log n)`。最优：排序 `O(n log n)` + 每个工作一次二分 `O(log n)`。

```python
def job_scheduling(start_time: list[int], end_time: list[int], profit: list[int]) -> int:
    jobs = sorted(zip(end_time, start_time, profit))     # 按结束时间排序
    ends = [end for end, _, _ in jobs]
    dp = [0] * (len(jobs) + 1)                           # dp[i]：只考虑前 i 份工作的最大报酬
    for i, (end, start, gain) in enumerate(jobs):
        # 结束时间 <= start 的工作有 k 份，正是排序后的前 k 份；end > start，所以 k <= i
        k = bisect_right(ends, start, 0, i)
        dp[i + 1] = max(dp[i], dp[k] + gain)             # 不做这份 / 做这份
    return dp[-1]
```

运行：`startTime=[1,2,3,3], endTime=[3,4,5,6], profit=[50,10,40,70]` → `120`，`startTime=[1,2,3,4,6], endTime=[3,5,10,6,9], profit=[20,20,100,70,60]` → `150`，`startTime=[1,1,1], endTime=[2,3,4], profit=[5,6,4]` → `6`，`startTime=[1], endTime=[2], profit=[7]` → `7`。

**复杂度。** 时间 `O(n log n)`：排序 `O(n log n)`，每份工作一次二分 `O(log n)`；空间 `O(n)`（排序后的数组、`ends`、`dp`）。

**易错点。**
- 二分用 `bisect_left` 而不是 `bisect_right`：「在 `X` 结束的可以接 `X` 开始的」，结束时间**等于**开始时间也兼容，必须把相等的算进前缀。示例 1 里 `[1,3]` 和 `[3,6]` 首尾相接，`bisect_left` 会漏掉它，输出 `70`（正确 `120`）。
- 没按**结束时间**排序（按开始时间排序）：前面可接的工作不再是一个前缀，`dp[k]` 的含义失效。
- 把 `dp` 当成「必须做第 `i` 份」的值而不取 `max(dp[i], …)`：不做这份工作也可能更优，`dp` 必须单调不减。

**追问。**
- 返回具体选了哪些工作：每步记下是否选了第 `i` 份和它接的前缀 `k`，从 `dp[n]` 往回走一遍。
- 最多做 `k` 份（LC 1751）：状态变成 `dp[j][i]`（用 `j` 份、看前 `i` 份），用完整二维表。
- 工作数很大时的在线版本：按开始时间排序 + 小顶堆（见另一种解法）。

**同模式。** LC 1751 参加会议 II（加「至多 `k` 个」）、LC 2008 出租车的最大盈利、LC 435 无重叠区间（无权重，贪心）、LC 646 最长数对链、LC 300 最长递增子序列（二分的另一个用法）。
