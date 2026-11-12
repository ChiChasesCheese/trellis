---
slug: longest-strictly-increasing-or-strictly-decreasing-subarray
---
## Q
**LC 3105 最长的严格递增或递减子数组**｜Easy

返回数组 `nums` 中严格递增或严格递减的最长非空子数组的长度。

## A
**一句话。** 一遍扫描，同时维护以当前元素结尾的递增长度和递减长度，断了就重置为 `1`。

```python
def longest_monotonic(nums):
    inc = dec = best = 1    # 以当前元素结尾的递增 / 递减长度
    for a, b in zip(nums, nums[1:]):
        inc = inc + 1 if b > a else 1
        dec = dec + 1 if b < a else 1
        best = max(best, inc, dec)
    return best
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 比较写成 `>=` / `<=`：相等也被接上，`[3,3,3,3]` 得 `4`，应为 `1`。
- 只用一个计数器、相邻不等就加一：升降混在一起，`[1,3,2]` 得 `3`，应为 `2`。

**追问。**
- 要返回子数组本身？：更新 `best` 时记下结尾下标，起点是结尾减长度加一。

**同模式。** LC 674 最长连续递增序列、LC 53 最大子数组和、LC 978 最长湍流子数组、LC 485 最大连续 1 的个数
