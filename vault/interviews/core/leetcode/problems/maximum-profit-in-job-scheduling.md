---
slug: maximum-profit-in-job-scheduling
---
## Q
**LC 1235 规划兼职工作**｜Hard

每份工作有开始、结束时间和报酬，时间重叠的不能同时做（首尾相接可以），求最大总报酬。

## A
**一句话。** 按结束时间排序做 DP，二分找到最后一份能接在前面的工作，取「不做 / 做」的较大值。

```python
def job_scheduling(start_time, end_time, profit):
    jobs = sorted(zip(end_time, start_time, profit))
    ends = [end for end, _, _ in jobs]
    dp = [0] * (len(jobs) + 1)   # dp[i]：前 i 份的最大报酬
    for i, (end, start, gain) in enumerate(jobs):
        # 结束时间 <= start 的恰好是前 k 份
        k = bisect_right(ends, start, 0, i)
        dp[i + 1] = max(dp[i], dp[k] + gain)
    return dp[-1]
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 用 `bisect_left`：结束时间等于开始时间也兼容，要算进前缀。`[1,3]` 接 `[3,6]` 的例子得 `70`，应为 `120`。
- 按开始时间排序：可接的工作不再是前缀，`dp[k]` 失效。
- `dp[i+1]` 不和 `dp[i]` 取最大：不做这份可能更优，`dp` 要单调不减。

**追问。**
- 不想二分怎么办？：按开始时间排序，小顶堆存「已开始未结束」的 `(结束时间, 报酬)`，新工作先弹出已结束的更新 `best`，再压入。
- 最多做 `k` 份（LC 1751）？：状态加一维 `dp[j][i]`。

**同模式。** LC 1751 最多可以参加的会议数目 II、LC 2008 出租车的最大盈利、LC 435 无重叠区间、LC 646 最长数对链
