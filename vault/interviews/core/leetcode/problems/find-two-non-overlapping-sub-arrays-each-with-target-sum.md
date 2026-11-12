---
slug: find-two-non-overlapping-sub-arrays-each-with-target-sum
---
## Q
**LC 1477 找两个和为目标值且不重叠的子数组**｜Medium

正整数数组 `arr`，找两个互不重叠、和都为 `target` 的子数组，返回长度之和的最小值，找不到返回 `-1`。

## A
**一句话。** 滑动窗口逐个找出和为 `target` 的子数组，`best[i]` 记 `arr[:i]` 里最短的目标子数组，用它和当前窗口配对。

```python
def min_sum_of_lengths(arr, target):
    n = len(arr)
    INF = n + 1
    best = [INF] * (n + 1)   # best[i]：arr[:i] 最短目标子数组
    ans = INF
    left = window = 0
    for r, x in enumerate(arr):
        window += x
        while window > target:
            window -= arr[left]
            left += 1
        best[r + 1] = best[r]
        if window == target:
            length = r - left + 1
            ans = min(ans, best[left] + length)  # 搭档在左边
            best[r + 1] = min(best[r + 1], length)
    return -1 if ans == INF else ans
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 直接取两个最短的相加：`[1,2,1]`、`target = 3` 中两个目标子数组重叠，应为 `-1`。
- 用 `best[r]` 配对：会把与当前窗口重叠的子数组当搭档，要用 `best[left]`。

**追问。**
- 元素有负数或零呢？：滑窗失效，改用前缀和加哈希表。
- 要选 `k` 个不重叠子数组呢？：状态 `dp[j][i]`（选 `j` 段、看前 `i` 个）。

**同模式。** LC 560 和为 K 的子数组、LC 209 长度最小的子数组、LC 1031 两个非重叠子数组的最大和、LC 2054 两个最好的不重叠活动
