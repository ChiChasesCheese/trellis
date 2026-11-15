---
slug: find-the-integer-added-to-array-i
---
## Q
**LC 3131 找出与数组相加的整数 I**｜Easy

两个等长数组 `nums1`、`nums2`。`nums1` 的每个元素都加上同一个整数 `x`（可正可负）后，与 `nums2` 包含相同的元素且频次相同。求 `x`。

## A
**一句话。** 两个数组各自的最小值对应，`x = min(nums2) - min(nums1)`。

```python
def added_integer(nums1, nums2):
    return min(nums2) - min(nums1)
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 用 `nums2[0] - nums1[0]`：数组没有对齐，只有最小值一定对应最小值。
- 用平均值之差：整数除法可能出错，最小值更直接。

**追问。**
- 允许 `nums1` 删两个元素（LC 3132）？：答案只可能出现在 `nums1` 较小的三个数里，枚举后校验。

**同模式。** LC 3132 找出与数组相加的整数 II、LC 392 判断子序列
