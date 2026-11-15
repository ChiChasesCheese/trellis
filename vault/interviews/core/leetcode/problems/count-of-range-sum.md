---
slug: count-of-range-sum
---
## Q
**LC 327 区间和的个数**｜Hard

给整数数组 `nums` 与 `[lower, upper]`，统计有多少个子数组（区间 `[i, j]`）的和落在 `[lower, upper]` 内。

## A
**一句话。** 转成前缀和：数满足 `lower ≤ pre[j] - pre[i] ≤ upper` 且 `i < j` 的对；在归并排序里，左半有序，右半每个 `pre[j]` 用两个指针数出左半里落在 `[pre[j]-upper, pre[j]-lower]` 的个数。

```python
def count_range_sum(nums, lower, upper):
    pre = [0]
    for x in nums:
        pre.append(pre[-1] + x)
    def sort(lo, hi):                  # 归并排序并计数
        if hi - lo <= 1:
            return 0
        mid = (lo + hi) // 2
        cnt = sort(lo, mid) + sort(mid, hi)
        l = r = lo
        for j in range(mid, hi):       # 左半 [lo, mid) 已有序
            while l < mid and pre[l] < pre[j] - upper:
                l += 1                 # 第一个 >= pre[j]-upper
            while r < mid and pre[r] <= pre[j] - lower:
                r += 1                 # 第一个 > pre[j]-lower
            cnt += r - l
        pre[lo:hi] = sorted(pre[lo:hi])   # 合并
        return cnt
    return sort(0, len(pre))
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 用 `nums` 本身而不是前缀和：子数组和要靠前缀和做差，且前缀和要含开头的 `0`。
- 边界开闭写反：`l` 用 `<`（含左端点），`r` 用 `<=`（含右端点），否则多数或少数。
- 先合并后计数：计数必须在合并前，那时左右两半各自有序但整体还没混。

**追问。**
- 还能怎么做？：离散化前缀和，用树状数组边扫边查「已出现的前缀和里落在 `[pre-upper, pre-lower]` 的个数」，同样 `O(n log n)`。
- 为什么与「右侧小于当前元素」同类？：都是在序列里数「后面某个量与前面某个量满足大小关系」的对，归并或树状数组统一解决。

**同模式。** LC 315 计算右侧小于当前元素的个数、LC 493 翻转对、LC 307 区域和检索 - 数组可修改、LC 560 和为 K 的子数组
