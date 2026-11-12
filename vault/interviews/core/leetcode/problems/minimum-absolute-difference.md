---
slug: minimum-absolute-difference
---
## Q
**LC 1200 最小绝对差**｜Easy

数组 `arr` 元素互不相同，按升序返回所有差等于最小绝对差的数对 `[a, b]`（`a < b`）。

## A
**一句话。** 排序后差最小的数对必相邻，先求最小相邻差，再收集等于它的数对。

```python
def minimum_abs_difference(arr):
    arr = sorted(arr)
    best = min(b - a for a, b in pairwise(arr))
    return [[a, b] for a, b in pairwise(arr)
            if b - a == best]
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 返回全部相邻对：`[1,3,6,10,15]` 得 4 对，应只有 `[[1,3]]`。
- 找到第一个最小差就停：`[4,2,1,3]` 三对差都是 `1`，要全部收集。

**追问。**
- 能不排序吗？：值域不大时用计数数组，`O(n+V)`。

**同模式。** LC 539 最小时间差、LC 164 最大间距、LC 532 数组中的 k-diff 数对
