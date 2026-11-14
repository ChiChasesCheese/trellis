---
slug: maximum-element-after-decreasing-and-rearranging
---
## Q
**LC 1846 减小和重新排列数组后的最大元素**｜Medium

正整数数组，可以把元素减小、任意重排，要求首元素为 `1` 且相邻差不超过 `1`，求可能的最大元素。

## A
**一句话。** 排序后从小到大，每个数最多只能是「前一个 + 1」，也不能超过原值：`prev = min(x, prev + 1)`。

```python
def maximum_element_after_decrementing_and_rearranging(arr):
    prev = 0
    for x in sorted(arr):
        prev = min(x, prev + 1)   # 只能减，不能比前一个高 2
    return prev
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 初值 `prev = 1`：第一个数应被压到 `1`，`prev = 0` 起步让 `min(x, 1)` 自然做到。
- 不排序直接扫：小数放后面会卡住前面的大数上升。

**追问。**
- `O(n)`？：计数排序，值大于 `n` 的当作 `n`；按值从小到大，`prev = min(prev + cnt[v], v)`。
- 为什么递增排列最优？：答案只看能爬多高，排序后每步都能尽量 `+1`。

**同模式。** LC 455 分发饼干、LC 945 使数组唯一的最小增量、LC 3397 执行操作后不同元素的最大数量
