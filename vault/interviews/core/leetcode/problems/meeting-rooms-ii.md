---
slug: meeting-rooms-ii
---
## Q
**LC 253 会议室 II**｜Medium

给会议区间 `[start, end]` 数组，求最少需要几间会议室；一场结束的时刻可以立刻开下一场。

## A
**一句话。** 按开始时间排序，小根堆存各在用房间的结束时间，最早结束的已结束就复用，否则新开。

```python
def min_meeting_rooms(intervals):
    ends = []                    # 小根堆：在用房间的结束时间
    for start, end in sorted(intervals):
        if ends and ends[0] <= start:
            heapq.heapreplace(ends, end)   # 复用：弹旧压新
        else:
            heapq.heappush(ends, end)      # 没有空房，新开一间
    return len(ends)
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 复用条件写成 `<`：`[[1,5],[5,9]]` 得 `2`，应为 `1`。
- 没按开始时间排序：`[[10,20],[0,5],[6,9]]` 得 `2`，应为 `1`。

**追问。**
- 还要给每场分配房间号？：堆里存 `(结束时间, 房间号)`，另用一个空闲房间号堆。
- 只问一个人能否参加全部会议（LC 252）？：排序后看相邻区间是否重叠。

**同模式。** LC 252 会议室、LC 2402 会议室 III、LC 435 无重叠区间、LC 1094 拼车
