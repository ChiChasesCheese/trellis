---
id: tlc-find-two-non-overlapping-sub-arrays-each-with-target-sum-2-code
node: b.find-two-non-overlapping-sub-arrays-each-with-target-sum
type: qa
step: 2
---
## Q
**LC 1477 找两个和为目标值且不重叠的子数组**｜写出 Python 实现

整数数组 `arr`（长度 `1 ~ 10^5`，元素 `1 ~ 1000`，全为正）和 `target`（`1 ~ 10^8`）。选出两个互不重叠、和都为 `target` 的子数组，返回它们长度之和的最小值，找不到返回 `-1`。要求 `O(n)`。

## A
**思路。** 滑动窗口维护和不超过 `target` 的窗口 `arr[left..right]`。`best[i]` 表示 `arr[:i]` 里和为 `target` 的最短子数组长度。每当窗口和恰好等于 `target`，当前子数组长度为 `length`；它左边（严格在 `left` 之前）的最短搭档是 `best[left]`，用 `best[left] + length` 更新答案，同时用 `length` 更新 `best[right + 1]`。

```python
def min_sum_of_lengths(arr: list[int], target: int) -> int:
    n = len(arr)
    INF = n + 1                                  # 任何真实答案都 <= n
    best = [INF] * (n + 1)                       # best[i]：arr[:i] 里和为 target 的最短子数组长度
    ans = INF
    left = window = 0                            # 窗口 arr[left..right]，元素全为正所以可以收缩
    for right, x in enumerate(arr):
        window += x
        while window > target:
            window -= arr[left]
            left += 1
        best[right + 1] = best[right]
        if window == target:
            length = right - left + 1
            ans = min(ans, best[left] + length)  # 前一段必须完全在 left 之前
            best[right + 1] = min(best[right + 1], length)
    return -1 if ans == INF else ans
```

运行：`[3,2,2,4,3], 3` → `2`，`[7,3,4,7], 7` → `2`，`[4,3,2,6,2,3,4], 6` → `-1`，`[5,5,4,4,5], 3` → `-1`，`[3,1,1,1,5,1,2,1], 3` → `3`，`[1,2,1], 3` → `-1`。

**复杂度。** 时间 `O(n)`：窗口两端各只前进 `n` 步；空间 `O(n)`（`best` 数组）。

**写法要点。** `best` 数组多开一格，`best[0] = INF` 表示「空前缀没有子数组」，下标含义是前缀长度，与 `left`、`right + 1` 对齐。整数哨兵 `INF = n + 1` 保证 `best[left] + length` 在没有搭档时一定不小于 `n + 2`，不会被误当成答案。滑动窗口用 `while window > target` 收缩，而不是 `if`，因为一个大元素可能需要弹出多个左元素。`enumerate` 同时给出下标和值。
