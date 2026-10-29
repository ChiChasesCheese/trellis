---
id: tlc-maximum-profit-in-job-scheduling-5-alt
node: a.maximum-profit-in-job-scheduling
type: qa
step: 5
---
## Q
**LC 1235 规划兼职工作**｜另一种解法

除了「按结束时间排序 + 二分」，规划兼职工作还有什么解法？暴力 DP 什么时候够用，什么时候该选哪种？

## A
**按开始时间排序 + 小顶堆**（扫描线，sweep line）。工作按开始时间处理；堆里放「已经开始、还没被结算」的工作 `(结束时间, 做完它的总报酬)`。处理下一份工作 `start` 前，把堆里 `end <= start` 的全部弹出，用它们的总报酬更新 `best`（这些工作已结束，都能接在新工作前面）；然后压入 `(end, best + gain)`。最后把堆清空再取一次最大值。

```python
def job_scheduling_heap(start_time: list[int], end_time: list[int], profit: list[int]) -> int:
    best = 0                                             # 已结算的最大报酬
    running: list[tuple[int, int]] = []                  # 小顶堆：(结束时间, 做完它的总报酬)
    for start, end, gain in sorted(zip(start_time, end_time, profit)):
        while running and running[0][0] <= start:        # 在 start 前结束的工作都能作为前驱
            best = max(best, heappop(running)[1])
        heappush(running, (end, best + gain))
    while running:
        best = max(best, heappop(running)[1])
    return best
```

时间 `O(n log n)`，空间 `O(n)`，与二分 DP 同阶，且不需要 `dp` 数组和 `ends`。

**暴力 DP**：按结束时间排序后，对每份工作线性扫描所有更早的工作找兼容者，`O(n^2)`；`n` 很小（几百以内）或只想快速写对时可用。

**怎么选。** 面试默认写排序 + `bisect_right` 的 DP：状态含义清楚，易扩展成「最多 `k` 份」和「返回方案」。堆解法适合工作按开始时间陆续到达的场景，扩展到带 `k` 的版本不方便。
