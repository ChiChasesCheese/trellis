---
slug: find-the-integer-added-to-array-ii
---
## Q
**LC 3132 找出与数组相加的整数 II**｜Medium

从 `nums1` 删掉两个数，再给剩下每个数加 `x`，得到的多重集合等于 `nums2`。求最小的 `x`（保证有解）。

## A
**一句话。** 两边排序，删后的最小值只可能是 `nums1[0..2]` 之一，于是 `x` 只有三个候选；从最小的候选试起，用判断子序列的双指针验证。

```python
def minimum_added_integer(nums1, nums2):
    nums1.sort()
    nums2.sort()
    for i in (2, 1, 0):         # nums1[i] 越大，x 越小
        x = nums2[0] - nums1[i]
        j = 0
        for v in nums1[i:]:     # nums2 是否 nums1[i:]+x 的子序列
            if j < len(nums2) and v + x == nums2[j]:
                j += 1
        if j == len(nums2):
            return x
```

**复杂度。** 时间 `O(n log n)`，空间 `O(1)`（不计排序）。

**易错点。**
- 候选从 `i=0` 试起：先找到的是最大的 `x`，题目要最小。
- 担心子序列匹配会多删：`nums1[i:]` 长 `n-i`，匹配完 `n-2` 个时恰好又删了 `2-i` 个，总数正好是 2。

**追问。**
- 删 `k` 个？：候选是 `nums1[0..k]`，共 `k+1` 个，每个 `O(n)` 验证。
- 不排序能做吗？：可以枚举候选 `x` 后用计数比较多重集合，但仍要知道最小的几个数。

**同模式。** LC 392 判断子序列、LC 3131 找出与数组相加的整数 I
