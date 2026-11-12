---
slug: merge-intervals
---
## Q
**LC 56 合并区间**｜Medium

合并所有重叠的区间（端点相接也算重叠），返回互不重叠的区间数组。

## A
**一句话。** 按起点排序，只和结果里最后一个区间比较：重叠就延长终点，否则另起新区间。

```python
def merge(intervals):
    merged = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:   # 相接也算重叠
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 重叠条件写 `<`：`[[1,4],[4,5]]` 得 `[[1,4],[4,5]]`，应为 `[[1,5]]`。
- 延长终点不取 `max`：`[[1,4],[2,3]]` 得 `[[1,3]]`，应为 `[[1,4]]`。
- 不排序：`[[1,2],[8,9],[2,3]]` 丢掉 `3`，应为 `[[1,3],[8,9]]`。

**追问。**
- 区间流式到达？：用按起点有序的列表加 `bisect` 维护已合并区间。
- 求覆盖的总长度？：合并后对 `end - start` 求和。

**同模式。** LC 57 插入区间、LC 435 无重叠区间、LC 253 会议室 II、LC 986 区间列表的交集
