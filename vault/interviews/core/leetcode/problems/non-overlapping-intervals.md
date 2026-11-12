---
slug: non-overlapping-intervals
---
## Q
**LC 435 无重叠区间**｜Medium

最少移除多少个区间，剩下的两两不重叠（只在端点接触不算重叠）。

## A
**一句话。** 最少移除等于最多保留：按右端点排序，起点不小于上一个保留区间的右端点就保留。

```python
def erase_overlap_intervals(intervals):
    kept, end = 0, -inf           # 保留数、最后保留区间的右端点
    intervals = sorted(intervals, key=itemgetter(1))
    for start, finish in intervals:
        if start >= end:          # 端点接触不算重叠
            kept += 1
            end = finish
    return len(intervals) - kept
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 按起点排序、遇重叠丢后来的：`[[1,100],[2,3],[4,5]]` 得 `2`，应为 `1`。
- `>=` 写成 `>`：`[[1,2],[2,3]]` 得 `1`，应为 `0`。
- `end` 初值写 `0`：起点可为负，会误丢区间。

**追问。**
- 区间带权重要最大权重？：按右端点排序加二分的 DP（LC 1235）。
- 与射气球（LC 452）有何不同？：同一个贪心，但那里端点接触算重叠，条件为 `>`。

**同模式。** LC 452 用最少数量的箭引爆气球、LC 56 合并区间、LC 646 最长数对链、LC 1353 最多可以参加的会议数目
