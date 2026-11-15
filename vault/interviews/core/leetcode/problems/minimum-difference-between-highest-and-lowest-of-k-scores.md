---
slug: minimum-difference-between-highest-and-lowest-of-k-scores
---
## Q
**LC 1984 学生分数的最小差值**｜Easy

整数数组 `nums`，从中选 `k` 名学生的分数，使所选分数的最高分与最低分之差最小，返回这个最小差。

## A
**一句话。** 排序后，选中的 `k` 个数在最优情形下是相邻的一段，滑动窗口取 `nums[i + k - 1] - nums[i]` 的最小值。

```python
def minimum_difference(nums, k):
    nums.sort()
    return min(nums[i + k - 1] - nums[i]
               for i in range(len(nums) - k + 1))
```

**复杂度。** 时间 `O(n log n)`，空间 `O(1)`。

**易错点。**
- 不排序直接滑窗：窗口里的最大最小值不再是两端。
- `k == 1`：窗口只有一个数，差为 `0`，上式自然返回 `0`。

**追问。**
- 为什么选相邻的一段就够？：任何选法的差都不小于同样最小值起点的相邻 `k` 个数的差。

**同模式。** LC 611 有效三角形的个数、LC 812 最大三角形面积、LC 561 数组拆分 I
