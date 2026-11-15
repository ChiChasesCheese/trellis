---
slug: maximum-product-of-two-elements-in-an-array
---
## Q
**LC 1464 数组中两元素的最大乘积**｜Easy

给整数数组 `nums`，选两个不同下标 `i`、`j`，使 `(nums[i] - 1) * (nums[j] - 1)` 最大，返回这个最大值。

## A
**一句话。** `nums` 全为正整数，`x - 1` 单调递增，乘积最大就是取最大的两个数；一遍扫描维护最大和次大。

```python
def max_product(nums):
    first = second = 0
    for x in nums:
        if x > first:
            first, second = x, first   # 新的最大值，旧的变次大
        elif x > second:
            second = x
    return (first - 1) * (second - 1)
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 把最大值和次大值取同一个下标：两个下标必须不同，`first`、`second` 来自不同元素。
- 忘了减 1：乘积是 `(a-1)(b-1)`，不是 `a * b`。
- 次大值初始化成大正数：从 `0` 起（元素都 `≥ 1`），否则 `elif` 分支进不去。

**追问。**
- 允许负数怎么办？：还要比较最小的两个数（两负相乘为正），类似 LC 628。
- 用排序行吗？：`sorted(nums)[-2:]`，`O(n log n)`，一遍扫描更快。

**同模式。** LC 628 三个数的最大乘积、LC 215 数组中的第 K 个最大元素、LC 152 乘积最大子数组
