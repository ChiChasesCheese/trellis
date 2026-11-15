---
slug: find-minimum-time-to-finish-all-jobs
---
## Q
**LC 1723 完成所有工作的最短时间**｜Hard

`jobs[i]` 是第 `i` 项工作所需时间，要分给 `k` 个工人，每项工作只给一个人。工人的工作时间是分到的工作之和，求所有分配方案里「最大工作时间」的最小值。

## A
**一句话。** 回溯：按从大到小依次把每项工作分给某个工人，用当前最优解剪枝，并跳过与已试过的工人负载相同的工人。

```python
def minimum_time_required(jobs, k):
    jobs.sort(reverse=True)      # 大的先分，更早触发剪枝
    load = [0] * k
    best = inf
    def dfs(i, cur_max):
        nonlocal best
        if cur_max >= best:
            return               # 已经不比当前最优好
        if i == len(jobs):
            best = cur_max
            return
        tried = set()
        for w in range(k):
            if load[w] in tried:
                continue         # 负载相同的工人等价
            tried.add(load[w])
            load[w] += jobs[i]
            dfs(i + 1, max(cur_max, load[w]))
            load[w] -= jobs[i]
    dfs(0, 0)
    return best
```

**复杂度。** 最坏 `O(k^n)`，剪枝后实际快得多；空间 `O(n + k)`。

**易错点。**
- 不排序、不去重：对 12 项工作、6 个工人会超时，这两项剪枝是关键。
- 回溯不恢复 `load[w]`：后续分支基于被污染的负载。
- 不剪枝已不优的分支：`cur_max >= best` 时直接返回。

**追问。**
- 另一种思路？：二分最大工作时间 `T`，用回溯判断能否把所有工作装进 `k` 个容量为 `T` 的桶（类似 LC 698）。
- 状态压缩 DP？：`dp[i][mask]` 前 `i` 个工人处理 `mask` 集合的最小最大值，枚举子集，`O(3^n k)`。

**同模式。** LC 698 划分为k个相等的子集、LC 473 火柴拼正方形、LC 2305 公平分发饼干、LC 416 分割等和子集
