---
slug: find-target-indices-after-sorting-array
---
## Q
**LC 2089 找出数组排序后的目标下标**｜Easy

返回 `nums` 排序后 `target` 所在的所有下标（递增），不存在则返回空列表。

## A
**一句话。** 排序后 `target` 占一段连续下标：起点是比它小的元素个数，长度是它的出现次数。

```python
def target_indices(nums, target):
    less = sum(x < target for x in nums)   # 起始下标
    equal = nums.count(target)             # 区间长度
    return list(range(less, less + equal)) # 不存在时为 []
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 起点用 `x <= target` 计数：`[1,2,5,2,3]`、`target=2` 得 `[3,4]`，应为 `[1,2]`。
- 返回原数组里的下标：得 `[1,3]`，题目要的是排序后的下标。

**追问。**
- 数组已有序呢？：用 `bisect_left` 和 `bisect_right` 取区间，`O(log n)`（LC 34）。
- 要查询很多个 `target` 怎么办？：排序一次后二分，或建计数表加前缀和。

**同模式。** LC 1365 有多少小于当前数字的数字、LC 34 在排序数组中查找元素的第一个和最后一个位置、LC 35 搜索插入位置
