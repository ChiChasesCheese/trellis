---
id: tlc-maximum-profit-in-job-scheduling-2-code
node: a.maximum-profit-in-job-scheduling
type: qa
step: 2
---
## Q
**LC 1235 规划兼职工作**｜写出 Python 实现

三个数组 `startTime`、`endTime`、`profit`（长度 `n <= 5 * 10^4`，时间到 `10^9`）描述 `n` 份工作，选一组两两不重叠的工作（首尾相接允许），使总报酬最大。要求 `O(n log n)`。

## A
**思路。** 工作按结束时间排序，`dp[i]` 表示前 `i` 份工作的最大报酬。对第 `i` 份：不做则 `dp[i]`；做则用二分找到最后一份结束时间 `<=` 它开始时间的工作（前 `k` 份都兼容），收益是 `dp[k] + profit`，两者取大。

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

**写法要点。** `sorted(zip(end, start, profit))` 一步把三个数组打包并按结束时间排序（元组按字典序比较，结束时间相同再比开始时间）。`bisect_right(ends, start, 0, i)` 的 `hi=i` 把搜索限制在当前工作之前：因为 `end > start`，结果天然 `<= i`，写上它只是让意图更明确。`for i, (end, start, gain) in enumerate(jobs)` 同时拿到下标和解包后的三元组。`dp` 多留一格 `dp[0] = 0` 表示「一份都不考虑」，省掉边界判断。
