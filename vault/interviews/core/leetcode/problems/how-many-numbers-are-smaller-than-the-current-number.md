---
slug: how-many-numbers-are-smaller-than-the-current-number
---
## Q
**LC 1365 有多少小于当前数字的数字**｜Easy

对 `nums` 中每个数 `nums[i]`，统计数组中比它小的数有多少个（元素值在 `0..100`）。

## A
**一句话。** 计数排序加前缀和：先数每个值出现几次，再累加得到「小于 `x` 的个数」。

```python
def smaller_numbers_than_current(nums):
    cnt = [0] * 102
    for x in nums:
        cnt[x + 1] += 1          # 错开一位，前缀和即「严格小于」
    for v in range(1, 102):
        cnt[v] += cnt[v - 1]
    return [cnt[x] for x in nums]
```

**复杂度。** 时间 `O(n + 值域)`，空间 `O(值域)`。

**易错点。**
- 不错开一位：`cnt[x]` 的前缀和包含 `x` 自己，得到的是小于等于。
- 数组开成 101：错开后下标最大是 101，需要 102 个位置。

**追问。**
- 值域很大怎么办？：排序加二分，或排序后用「首次出现的位置」，`O(n log n)`。
- 重复值怎么处理？：相同的数答案相同，前缀和天然满足。

**同模式。** LC 1331 数组序号转换、LC 506 相对名次、LC 912 排序数组、LC 315 计算右侧小于当前元素的个数
