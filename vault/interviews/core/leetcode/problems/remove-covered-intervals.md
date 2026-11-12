---
slug: remove-covered-intervals
---
## Q
**LC 1288 删除被覆盖区间**｜Medium

区间 `[a,b)` 被 `[c,d)` 覆盖当且仅当 `c <= a` 且 `b <= d`。删掉被覆盖的区间，求剩下几个。

## A
**一句话。** 起点升序、同起点终点降序排序，扫描时终点超过已见最大终点才保留。

```python
def remove_covered_intervals(intervals):
    intervals.sort(key=lambda iv: (iv[0], -iv[1]))
    kept = 0
    max_end = 0
    for _, end in intervals:
        if end > max_end:      # 超出前面所有区间：没被覆盖
            kept += 1
            max_end = end
    return kept
```

**复杂度。** 时间 `O(n log n)`，空间 `O(1)`。

**易错点。**
- 同起点终点升序（默认排序）：`[[1,2],[1,4]]` 得 `2`，应为 `1`。
- 终点相等也保留（`>=`）：`[[1,4],[2,4]]` 得 `2`，应为 `1`。

**追问。**
- 要返回剩下的区间本身？：扫描时把保留的区间追加到结果里。
- 为什么同起点要让长的在前？：这样短的紧随其后，终点不超过已见最大值，被识别为覆盖。

**同模式。** LC 56 合并区间、LC 435 无重叠区间、LC 452 用最少数量的箭引爆气球、LC 57 插入区间
