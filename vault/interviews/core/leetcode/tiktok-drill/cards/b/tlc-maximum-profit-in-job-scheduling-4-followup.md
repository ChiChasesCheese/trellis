---
id: tlc-maximum-profit-in-job-scheduling-4-followup
node: b.maximum-profit-in-job-scheduling
type: qa
step: 4
---
## Q
**LC 1235 规划兼职工作**｜追问

面试官接着问：（1）要返回具体选了哪些工作？（2）改成**最多做 `k` 份**（LC 1751）？（3）为什么不能直接开一个按时间下标的数组做 DP？分别怎么改。

## A
1. **返回方案**：每算一个 `dp[i+1]` 就记下是否选了第 `i` 份、它接的前缀是 `k`，最后从 `dp[n]` 往回走。排序时把原下标也塞进元组：

```python
def job_scheduling_path(start_time: list[int], end_time: list[int], profit: list[int]) -> tuple[int, list[int]]:
    jobs = sorted(zip(end_time, start_time, profit, range(len(profit))))
    ends = [job[0] for job in jobs]
    dp = [0] * (len(jobs) + 1)
    took = [-1] * (len(jobs) + 1)               # took[i+1] = k 表示选了第 i 份且接在前 k 份之后
    for i, (end, start, gain, _) in enumerate(jobs):
        k = bisect_right(ends, start, 0, i)
        if dp[k] + gain > dp[i]:
            dp[i + 1], took[i + 1] = dp[k] + gain, k
        else:
            dp[i + 1] = dp[i]
    picked: list[int] = []
    i = len(jobs)
    while i > 0:
        if took[i] >= 0:
            picked.append(jobs[i - 1][3])
            i = took[i]
        else:
            i -= 1
    return dp[-1], picked[::-1]
```

2. **最多 `k` 份**：状态加一维，`dp[j][i]` 表示用至多 `j` 份、只看前 `i` 份的最大值，转移 `dp[j][i+1] = max(dp[j][i], dp[j-1][k] + gain)`，`k` 的二分不变。用完整二维表，时间 `O(nk + n log n)`；空间可以压到 `O(n)`：见 Python 工具箱「DP 降维」。
3. **时间下标数组**：时间到 `10^9`，数组放不下；只有 `n` 个关键点，所以排序 + 二分（或坐标压缩）。

**Python 提醒**：`bisect_right` 的 `key=` 参数（3.10+）可以直接对 `jobs` 二分而省掉 `ends`，但每次比较要多调一次函数；`sorted(zip(...))` 按元组字典序比较，原下标放在最后，只在前三项完全相同时才参与比较。
