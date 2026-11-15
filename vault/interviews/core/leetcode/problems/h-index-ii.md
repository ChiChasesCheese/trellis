---
slug: h-index-ii
---
## Q
**LC 275 H 指数 II**｜Medium

`citations` 是研究者各篇论文被引用次数，已按升序排列。h 指数是最大的 `h`：至少有 `h` 篇论文各被引用至少 `h` 次。要求 `O(log n)`。

## A
**一句话。** 对下标 `i`，后面（含自己）共 `n - i` 篇都不少于 `citations[i]`；找到第一个满足 `citations[i] >= n - i` 的 `i`，答案就是 `n - i`。

```python
def h_index(citations):
    n = len(citations)
    lo, hi = 0, n                # i 可以等于 n，表示 h = 0
    while lo < hi:
        mid = (lo + hi) // 2
        if citations[mid] >= n - mid:
            hi = mid             # mid 合格，试更靠左的
        else:
            lo = mid + 1
    return n - lo
```

**复杂度。** 时间 `O(log n)`，空间 `O(1)`。

**易错点。**
- 把 `h` 当成下标直接二分：要比较的是「被引次数」和「篇数」，篇数是 `n - mid`。
- `hi` 取 `n - 1`：所有论文都不够时应返回 0，需要 `lo` 能到达 `n`。
- 条件写成 `>`：恰好相等时 `h = n - mid` 就是合法答案。

**追问。**
- 为什么能二分？：`citations[i]` 随 `i` 增大，`n - i` 随 `i` 增大而减小，条件一旦成立就一直成立。
- 无序版本（LC 274）呢？：排序后用同样公式，或者计数排序做到 `O(n)`。

**同模式。** LC 274 H 指数、LC 34 在排序数组中查找元素的第一个和最后一个位置、LC 35 搜索插入位置、LC 1011 在 D 天内送达包裹的能力
