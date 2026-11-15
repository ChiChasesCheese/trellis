---
slug: count-pairs-whose-sum-is-less-than-target
---
## Q
**LC 2824 统计和小于目标的下标对数目**｜Easy

整数数组 `nums` 和目标 `target`。求下标对 `(i, j)` 的数目，满足 `0 <= i < j < n` 且 `nums[i] + nums[j] < target`。

## A
**一句话。** 排序后双指针：`nums[l] + nums[r] < target` 时，`l` 与 `l+1..r` 的所有数配都满足，加上 `r - l` 对并右移 `l`；否则左移 `r`。

```python
def count_pairs(nums, target):
    nums.sort()
    l, r = 0, len(nums) - 1
    ans = 0
    while l < r:
        if nums[l] + nums[r] < target:
            ans += r - l            # l 与 (l, r] 内每个数都满足
            l += 1
        else:
            r -= 1
    return ans
```

**复杂度。** 时间 `O(n log n)`，空间 `O(1)`。

**易错点。**
- 满足时只加 `1`：右边比 `r` 小的数配 `nums[l]` 也满足，要加 `r - l`。
- 不排序：下标对只关心数值，可以放心排序。

**追问。**
- 为什么排序不影响答案？：统计的是无序对，不依赖原下标的相对位置。

**同模式。** LC 167 两数之和 II - 输入有序数组、LC 15 三数之和、LC 1099 小于 K 的两数之和
