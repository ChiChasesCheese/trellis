---
id: tlc-max-consecutive-ones-iii-2-code
node: a.max-consecutive-ones-iii
type: qa
step: 2
---
## Q
**LC 1004 最大连续1的个数 III**｜写出 Python 实现

二进制数组 `nums`（长度 `1` 到 `10^5`，元素只有 `0` 和 `1`）和整数 `k`（`0 <= k <= nums.length`）。最多把 `k` 个 `0` 翻成 `1`，返回连续 `1` 的最大个数。要求 `O(n)`。

## A
**思路。** 求「至多含 `k` 个 `0` 的最长子数组」。右端逐个前进并统计窗口内的 `0`；一旦 `0` 的个数超过 `k`，就右移左端，直到窗口重新合法；每步用窗口长度更新答案。

```python
def longest_ones(nums: list[int], k: int) -> int:
    best = left = zeros = 0                # 窗口 nums[left : right + 1]，zeros 是窗口内 0 的个数
    for right, x in enumerate(nums):
        if x == 0:
            zeros += 1
        while zeros > k:                   # 0 太多：缩左端直到窗口合法
            if nums[left] == 0:
                zeros -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
```

运行：`[1,1,1,0,0,0,1,1,1,1,0]`、`k = 2` → `6`；`[0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1]`、`k = 3` → `10`；`[0,0,0]`、`k = 0` → `0`；`[0,0,0]`、`k = 3` → `3`；`[1]`、`k = 0` → `1`。

**复杂度。** 时间 `O(n)`：`right` 走 `n` 步，`left` 总共最多走 `n` 步；空间 `O(1)`。

**写法要点。** `enumerate` 同时拿下标和值；`best = left = zeros = 0` 链式赋值只用于不可变的整数；统计「窗口里有几个 0」只用一个计数器，不需要 `Counter` 或切片 `nums[left:right+1].count(0)`（后者每步 `O(窗口长度)`，整体退化成 `O(n^2)`）。
