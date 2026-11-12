---
slug: meeting-rooms
---
## Q
**LC 252 会议室**｜Easy

给会议区间 `intervals`，判断一个人能否参加全部会议（首尾相接不算重叠）。

## A
**一句话。** 按开始时间排序，只检查相邻会议：前一个的结束不晚于后一个的开始。

```python
def can_attend_meetings(intervals):
    a = sorted(intervals)
    return all(p[1] <= c[0] for p, c in pairwise(a))
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 不排序直接查相邻：`[[7,10],[2,4]]` 得 `False`，应为 `True`。
- 把首尾相接当重叠（写成 `<`）：`[[1,2],[2,3]]` 得 `False`，应为 `True`。

**追问。**
- 最少要几间会议室？：排序后用小根堆存结束时间，开始时间不早于堆顶就复用，否则新开一间（LC 253）。
- 在线插入新会议？：`bisect` 定位后只查前后两个邻居。

**同模式。** LC 253 会议室 II、LC 56 合并区间、LC 435 无重叠区间
