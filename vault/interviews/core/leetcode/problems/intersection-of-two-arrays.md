---
slug: intersection-of-two-arrays
---
## Q
**LC 349 两个数组的交集**｜Easy

返回 `nums1` 与 `nums2` 的交集，结果中每个元素唯一，顺序不限。

## A
**一句话。** 一个数组建集合，另一个逐个查成员，集合顺便去重。

```python
def intersection(nums1, nums2):
    return list(set(nums1).intersection(nums2))
```

**复杂度。** 时间 `O(n+m)`，空间 `O(n)`。

**易错点。**
- 用列表推导 `[x for x in nums1 if x in nums2]`：不去重，`[1,2,2,1]` 与 `[2,2]` 得 `[2,2]`，且 `in` 查列表是 `O(m)`。
- 误用 `Counter` 交集：保留重复次数，那是 LC 350 的答案。

**追问。**
- 两个数组都已排序怎么办？：双指针各走一步，相等取值并跳过重复，空间 `O(1)`。

**同模式。** LC 350 两个数组的交集 II、LC 217 存在重复元素、LC 1 两数之和
