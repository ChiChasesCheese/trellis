---
slug: count-subarrays-with-fixed-bounds
---
## Q
**LC 2444 统计定界子数组的数目**｜Hard

数组 `nums` 里，最小值恰为 `minK`、最大值恰为 `maxK` 的子数组有多少个？

## A
**一句话。** 固定右端点 `i`，左端点必须在最近越界位置之后、且不晚于最近的 `minK` 和 `maxK`。

```python
def count_subarrays(nums, min_k, max_k):
    ans = 0
    bad = lo = hi = -1   # 最近的越界、minK、maxK 的下标
    for i, x in enumerate(nums):
        if x < min_k or x > max_k:
            bad = i
        if x == min_k:
            lo = i
        if x == max_k:
            hi = i
        ans += max(0, min(lo, hi) - bad)
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 漏掉 `max(0, …)`：`[1,7,5]` 里 `min(lo,hi) < bad`，会加负数。
- 把 `x == max_k` 写成 `elif`：`minK == maxK` 时要同时更新两个下标，`[1,1,1,1]` 得 `0`（应为 `10`）。
- 初值用 `0` 不用 `-1`：下标 0 开头的子数组被少算。

**追问。**
- 只要求最大值等于 `maxK`？：只留 `bad` 和 `hi`，每步加 `max(0, hi - bad)`。
- 条件改成最大减最小 `<= k`？：下标法失效，用两个单调队列维护窗口最值（LC 2762）。

**同模式。** LC 2762 不间断子数组、LC 713 乘积小于 K 的子数组、LC 992 K 个不同整数的子数组、LC 930 和相同的二元子数组
