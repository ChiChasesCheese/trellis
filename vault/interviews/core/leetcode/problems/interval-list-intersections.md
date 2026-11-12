---
slug: interval-list-intersections
---
## Q
**LC 986 区间列表的交集**｜Medium

两个各自有序且内部不相交的闭区间列表，求它们的交集区间列表。

## A
**一句话。** 双指针同扫：交集是 `[max(起点), min(终点)]`，非空就收，然后终点较小的那个指针前进。

```python
def interval_intersection(first, second):
    i = j = 0
    ans = []
    while i < len(first) and j < len(second):
        lo = max(first[i][0], second[j][0])
        hi = min(first[i][1], second[j][1])
        if lo <= hi:                 # 闭区间，单点也算
            ans.append([lo, hi])
        if first[i][1] < second[j][1]:
            i += 1                   # 终点小的不会再相交
        else:
            j += 1
    return ans
```

**复杂度。** 时间 `O(m+n)`，空间 `O(1)`。

**易错点。**
- 两个指针一起前进：`[[1,10]]` 与 `[[2,3],[5,6]]` 漏掉 `[5,6]`。
- 用 `lo < hi` 判空：`[[1,3],[5,9]]` 与 `[[3,5]]` 应得 `[[3,3],[5,5]]`。

**追问。**
- `k` 个列表求公共交集？：`reduce` 逐个折叠，结果只会越来越短。
- 输入未排序或会重叠？：先各自排序合并，再用本解，总 `O(m log m + n log n)`。

**同模式。** LC 56 合并区间、LC 57 插入区间、LC 253 会议室 II、LC 1229 安排会议日程
