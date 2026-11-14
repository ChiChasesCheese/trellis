---
slug: maximum-subsequence-score
---
## Q
**LC 2542 最大子序列的分数**｜Medium

在两个等长数组中选同样的 `k` 个下标，分数是选中 `nums1` 之和乘以选中 `nums2` 的最小值，求最大分数。

## A
**一句话。** 按 `nums2` 从大到小枚举谁当最小值，前面见过的都不比它小；在这些里取 `nums1` 最大的 `k` 个，用小根堆维护和。

```python
def max_score(nums1, nums2, k):
    pairs = sorted(zip(nums2, nums1), reverse=True)
    h, total, ans = [], 0, 0
    for mn, x in pairs:        # mn 当最小值
        heappush(h, x)
        total += x
        if len(h) > k:
            total -= heappop(h)   # 去掉最小的 nums1
        if len(h) == k:
            ans = max(ans, total * mn)
    return ans
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 先算分数再入堆：当前元素不在所选的 `k` 个里，乘的 `mn` 不是这组的最小值。
- 用大根堆：要淘汰的是最小的 `nums1`，用小根堆。

**追问。**
- 为什么按 `nums2` 降序？：枚举最小值后，其余 `k-1` 个只能从更大的里选，选 `nums1` 最大的即可。
- 同构题（LC 1383）？：速度和效率换个名字，`k` 变成「至多 `k` 个」。

**同模式。** LC 215 数组中的第K个最大元素、LC 1383 最大的团队表现值、LC 857 雇佣 K 名工人的最低成本
