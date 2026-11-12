---
slug: h-index
---
## Q
**LC 274 H 指数**｜Medium

`citations[i]` 是第 `i` 篇论文的引用数，返回最大的 `h`，使至少有 `h` 篇论文引用数不小于 `h`。

## A
**一句话。** `h` 不会超过论文数 `n`，用计数桶（引用数 `>= n` 并入一桶）从大到小累加，第一个 `papers >= h` 的 `h` 就是答案。

```python
def h_index(citations):
    n = len(citations)
    bucket = [0] * (n + 1)       # bucket[c]：引用数为 c 的论文数
    for c in citations:
        bucket[min(c, n)] += 1
    papers = 0                   # 引用数 >= h 的论文数
    for h in range(n, 0, -1):
        papers += bucket[h]
        if papers >= h:
            return h
    return 0
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 桶下标不截断：`n=1` 而引用数为 `1000`，越界，要用 `min(c, n)`。
- `h` 是篇数不是引用数：`[100]` 的答案是 `1`。
- 排序版条件写成 `cs[h] >= h`：`[1,3,1]` 降序 `[3,1,1]` 会得 `2`，应为 `1`。

**追问。**
- 排序版怎么写？：降序后找最大的 `h` 使 `cs[h-1] >= h`，`O(n log n)`。
- 已排序时（LC 275）？：二分，`O(log n)`。

**同模式。** LC 275 H 指数 II、LC 169 多数元素、LC 1122 数组的相对排序、LC 347 前 K 个高频元素
