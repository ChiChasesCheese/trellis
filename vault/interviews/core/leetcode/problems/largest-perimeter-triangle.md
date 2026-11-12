---
slug: largest-perimeter-triangle
---
## Q
**LC 976 三角形的最大周长**｜Easy

从 `nums` 里选三条线段组成面积不为零的三角形，返回最大周长，组不成返回 `0`。

## A
**一句话。** 从大到小排序，检查相邻三元组 `a >= b >= c`，第一个满足 `b + c > a` 的周长最大。

```python
def largest_perimeter(nums):
    nums = sorted(nums, reverse=True)
    for a, b, c in zip(nums, nums[1:], nums[2:]):
        if b + c > a:
            return a + b + c
    return 0
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 只看最大的三条：`[2,3,4,10]` 得 `0`，应为 `9`。
- 写成 `b + c >= a`：等号时三点共线，`[1,2,1,10]` 得 `4`，应为 `0`。

**追问。**
- 为什么只看相邻三元组？：固定最长边 `a`，要让 `b + c` 最大，取紧挨着的两个最大值。
- 数三角形的个数（LC 611）？：排序后固定最长边，双指针 `O(n^2)`。

**同模式。** LC 611 有效三角形的个数、LC 812 最大三角形面积、LC 1984 学生分数的最小差值
