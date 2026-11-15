---
slug: find-anagram-mappings
---
## Q
**LC 760 找出变位映射**｜Easy

`nums2` 是 `nums1` 的变位（可含重复数字）。返回数组 `P`，使 `nums1[i]` 出现在 `nums2[P[i]]`，每个 `nums2` 下标只能被用一次。

## A
**一句话。** 哈希表记录每个值在 `nums2` 中的下标列表，遍历 `nums1` 时各弹出一个下标。

```python
def anagram_mappings(nums1, nums2):
    pos = defaultdict(list)
    for j, x in enumerate(nums2):
        pos[x].append(j)
    return [pos[x].pop() for x in nums1]   # 每个下标只用一次
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 用 `nums2.index(x)`：重复值总映射到同一个下标，违反「只用一次」，而且 `O(n²)`。
- 用 `dict[x] = j` 保存：后写的覆盖先写的，重复值只剩一个下标。

**追问。**
- 没有重复值时更简单吗？：直接 `{x: j}` 一个字典就够。

**同模式。** LC 242 有效的字母异位词、LC 49 字母异位词分组、LC 1 两数之和
