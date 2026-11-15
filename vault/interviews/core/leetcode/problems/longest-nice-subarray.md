---
slug: longest-nice-subarray
---
## Q
**LC 2401 最长优雅子数组**｜Medium

正整数数组 `nums`，若子数组里任意两个不同位置的数按位与都为 `0`，称为优雅子数组。求最长优雅子数组的长度。

## A
**一句话。** 不定长滑窗，用一个 `mask` 记窗口内所有数的 OR；新数与 `mask` 有公共位就从左边移出，移出用异或。

```python
def longest_nice_subarray(nums):
    ans = left = mask = 0
    for right, x in enumerate(nums):
        while mask & x:           # 有公共位：缩左端
            mask ^= nums[left]    # 位互不重叠，异或即移出
            left += 1
        mask |= x
        ans = max(ans, right - left + 1)
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 只和前一个数比 AND：要求两两为 `0`，必须和整个窗口的 OR 比。
- 先 `mask |= x` 再判断：`mask & x` 恒不为 `0`，窗口会被清空。

**追问。**
- 窗口最长能有多长？：每个数至少占一位且互不重叠，`nums[i] <= 10^9` 时最多 30 个，暴力向左扫 30 步也行。
- 为什么异或能移出？：窗口内各数的位互不相交，OR 等于和，异或掉一个数正好去掉它的位。

**同模式。** LC 3 无重复字符的最长子串、LC 1004 最大连续1的个数 III、LC 2958 最多 K 个重复元素的最长子数组
