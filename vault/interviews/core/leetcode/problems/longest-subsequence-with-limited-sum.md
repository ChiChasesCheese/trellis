---
slug: longest-subsequence-with-limited-sum
---
## Q
**LC 2389 和有限的最长子序列**｜Easy

整数数组 `nums` 和查询数组 `queries`。对每个 `queries[i]`，求 `nums` 的子序列中，元素和不超过 `queries[i]` 的最长长度。

## A
**一句话。** 子序列只看元素不看顺序：排序后优先取小的，前缀和单调递增，对每个查询二分找到前缀和不超过它的最长前缀。

```python
def answer_queries(nums, queries):
    nums.sort()
    pre, s = [], 0
    for x in nums:
        s += x
        pre.append(s)
    return [bisect_right(pre, q) for q in queries]
```

**复杂度。** 时间 `O((n + q) log n)`，空间 `O(n)`。

**易错点。**
- 用 `bisect_left`：前缀和恰好等于 `q` 时也满足，要用 `bisect_right`。
- 没排序：最长子序列要从最小元素开始取。

**追问。**
- 为什么子序列顺序无所谓？：只关心元素和与个数，选哪些元素不依赖顺序。

**同模式。** LC 1498 满足条件的子序列数目、LC 475 供暖器、LC 2300 咒语和药水的成功对数
