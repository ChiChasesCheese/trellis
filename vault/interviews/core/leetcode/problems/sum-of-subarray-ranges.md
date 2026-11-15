---
slug: sum-of-subarray-ranges
---
## Q
**LC 2104 子数组范围和**｜Medium

子数组的范围是其最大值与最小值之差。给整数数组 `nums`，返回所有子数组范围之和。

## A
**一句话。** 范围和 = 所有子数组最大值之和 − 所有子数组最小值之和；每个数作为最大（最小）值的子数组个数，用单调栈求左右边界得到。

```python
def sub_array_ranges(nums):
    n = len(nums)
    def total(pop):                    # 所有子数组「最值」之和
        left, right, st = [-1] * n, [n] * n, []
        for i, x in enumerate(nums):
            while st and pop(nums[st[-1]], x):
                right[st.pop()] = i    # 右边第一个更大(小)的位置
            left[i] = st[-1] if st else -1
            st.append(i)
        return sum(v * (i - left[i]) * (right[i] - i)
                   for i, v in enumerate(nums))
    return (total(lambda a, b: a < b)      # 最大值之和
            - total(lambda a, b: a > b))   # 最小值之和
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 重复值两边都用严格比较：同一个子数组会被两个相等的最大值各算一次，一边严格、一边非严格才不重不漏。
- 个数写成 `(i - left) + (right - i)`：左端点 `i - left` 种、右端点 `right - i` 种，应相乘。
- 求最大值和最小值用同一个比较方向：最大值弹出「更小」的，最小值弹出「更大」的，两次符号相反。

**追问。**
- 数据规模小时，暴力怎么写？：外层枚举左端点、内层右端点，同时更新当前最大最小值，`O(n²)`。
- 为什么 `left[i]` 取栈顶？：弹出所有更小的后，栈顶是左边第一个不小于 `x` 的位置，也就是该值作最大值的左边界。

**同模式。** LC 907 子数组的最小值之和、LC 2281 巫师的总力量和、LC 84 柱状图中最大的矩形、LC 739 每日温度
