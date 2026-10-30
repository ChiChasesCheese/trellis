---
id: tlc-meeting-rooms-4-followup
node: b.meeting-rooms
type: qa
step: 4
---
## Q
**LC 252 会议室**｜追问

面试官接着问：（1）最少需要多少间会议室（LC 253）？（2）会议一个一个在线加入，每次要立即判断是否冲突？（3）数据量大到排序也放不下？

## A
1. **最少会议室**：排序后用小根堆存各房间的结束时间。新会议的开始时间不早于堆顶，就复用那间房（`heapreplace`），否则新开一间。
```python
import heapq

def min_meeting_rooms(intervals: list[list[int]]) -> int:
    ends: list[int] = []                                 # 小根堆：每间正在用的会议室的结束时间
    for start, end in sorted(intervals):
        if ends and ends[0] <= start:
            heapq.heapreplace(ends, end)                 # 复用最早空出来的房间
        else:
            heapq.heappush(ends, end)                    # 没有空房间，新开一间
    return len(ends)
```
`[[0,30],[5,10],[15,20]]` → `2`，`[[7,10],[2,4]]` → `1`，`[[1,2],[2,3]]` → `1`。时间 `O(n log n)`。
2. **在线插入**：维护一个按起点有序的列表，`bisect.bisect_left` 找到插入位置，只和前后两个邻居比较，通过再 `insort`。查找 `O(log n)`，列表插入 `O(n)`；要整体 `O(log n)` 用平衡树（Python 里可用 `sortedcontainers.SortedList`，面试里说明即可）。
3. **放不下**：外部排序（分块排序再归并）；或按时间轴分桶，每桶内独立判断，桶边界处额外检查跨桶的会议。

**Python 提醒**：`intervals.sort()` 会改变调用方传入的列表；需要保持入参不变时用 `sorted(intervals)`。
