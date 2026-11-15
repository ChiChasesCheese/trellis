---
slug: sort-array-by-increasing-frequency
---
## Q
**LC 1636 按照频率将数组升序排序**｜Easy

按每个值出现的频率升序排序数组；频率相同的值按数值降序排列，返回排序后的数组。

## A
**一句话。** 先数频率，再用复合键 `(频率, -值)` 排序：频率小的在前，同频时值大的在前。

```python
def frequency_sort(nums):
    cnt = Counter(nums)
    return sorted(nums, key=lambda x: (cnt[x], -x))
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 同频时按值升序：题目要求降序，键里要取 `-x`。
- 去重后排序：结果要保留每个值的全部出现次数，对原数组排序，不是对去重后的键排序。
- 先按值排序再按频率排序但不稳定：Python 的排序稳定，复合键更直接。

**追问。**
- 不用 `-x` 怎么写降序？：`sorted(nums, key=lambda x: cnt[x])` 前先 `nums.sort(reverse=True)`，利用排序稳定性。
- 频率排序想 `O(n)`？：频率最多 `n`，桶排序，同频桶内再按值处理。

**同模式。** LC 451 根据字符出现频率排序、LC 347 前 K 个高频元素、LC 692 前K个高频单词、LC 1366 通过投票对团队排名
