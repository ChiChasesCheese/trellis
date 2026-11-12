---
slug: insert-interval
---
## Q
**LC 57 插入区间**｜Medium

给按起点升序、互不重叠的区间列表和一个新区间，插入后必要时合并，返回仍有序且不重叠的列表。端点相等也算重叠。

## A
**一句话。** 一次线性扫描分三段：左边不重叠的原样放，重叠的并入新区间，右边的原样放。

```python
def insert(intervals, newInterval):
    start, end = newInterval
    res, i, n = [], 0, len(intervals)
    while i < n and intervals[i][1] < start:   # 在左边
        res.append(intervals[i])
        i += 1
    while i < n and intervals[i][0] <= end:    # 重叠：并入
        start = min(start, intervals[i][0])
        end = max(end, intervals[i][1])
        i += 1
    res.append([start, end])
    return res + intervals[i:]                 # 在右边
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 第一段写成 `<=`：`[[1,5]]` 加 `[5,8]` 得 `[[1,5],[5,8]]`，应为 `[[1,8]]`，端点相等算重叠。
- 合并时直接赋值而不取 `min` 和 `max`：`[[3,5]]` 加 `[0,4]` 得 `[[3,5]]`，应为 `[[0,5]]`。

**追问。**
- 为什么不用排序再合并？：列表已有序，扫描即可，`O(n)` 优于 `O(n log n)`。
- 只判断能否无重叠插入（LC 729）？：二分找前后邻居。

**同模式。** LC 56 合并区间、LC 435 无重叠区间、LC 986 区间列表的交集、LC 252 会议室
