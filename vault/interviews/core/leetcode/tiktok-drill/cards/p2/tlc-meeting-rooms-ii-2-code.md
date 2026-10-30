---
id: tlc-meeting-rooms-ii-2-code
node: p2.meeting-rooms-ii
type: qa
step: 2
---
## Q
**LC 253 会议室 II**｜写出 Python 实现

`intervals[i] = [start_i, end_i]` 是会议时间，`1 <= intervals.length <= 10^4`，`0 <= start_i < end_i <= 10^6`。一个会议结束的时刻可以立刻开始另一个会议，返回所需会议室的最少数量。

## A
**思路。** 按开始时间排序。小根堆存各个正在使用的房间的结束时间。新会议到来时，如果堆顶（最早结束）不晚于它的开始时间，就复用那间房，把堆顶换成新会议的结束时间；否则新开一间。堆的大小就是答案。

```python
import heapq


def min_meeting_rooms(intervals: list[list[int]]) -> int:
    ends: list[int] = []                           # 小根堆：每个在用会议室的结束时间
    for start, end in sorted(intervals):
        if ends and ends[0] <= start:              # 最早结束的会议已结束：复用它的房间
            heapq.heapreplace(ends, end)           # 弹出旧结束时间并压入新的，一次 O(log n)
        else:
            heapq.heappush(ends, end)              # 没有空房间：新开一间
    return len(ends)                               # 堆里剩几个 = 同时在用的房间数峰值
```

运行：`[[0,30],[5,10],[15,20]]` → `2`；`[[7,10],[2,4]]` → `1`；`[[1,5],[5,9]]` → `1`；`[[1,2]]` → `1`；`[[1,5],[1,5],[1,5]]` → `3`。

**复杂度。** 时间 `O(n log n)`：排序 `O(n log n)`，每个会议至多一次堆操作 `O(log n)`；空间 `O(n)`。

**写法要点。** `heapq.heapreplace(heap, x)` 先弹出堆顶再压入 `x`，比 `heappop` 加 `heappush` 少一次调整；`ends and ends[0] <= start` 先判堆非空再看堆顶；`sorted(intervals)` 对 `[start, end]` 按字典序排，起点相同再比终点；堆里只放整数，因此不用担心比较不了的元素。
