---
id: tlc-core-meeting-rooms-ii
node: p2.meeting-rooms-ii
type: qa
---
## Q
**LC 253 会议室 II**｜Medium · LC TikTok 近 3 个月热度 95/100（全时段 88） · 近一年被问：美国 2 次、国内 1 次 · CodeTop 国内累计 16 次 · 最近 2026-10（美国面试记录） · 也在：Amazon、Blind 75、NeetCode 150

给一个会议时间数组 `intervals`，`intervals[i] = [start_i, end_i]`，返回需要的最少会议室数量。一个会议结束的时刻可以立刻开始下一个会议。`1 <= intervals.length <= 10^4`，`0 <= start_i < end_i <= 10^6`。例：`[[0,30],[5,10],[15,20]]` → `2`；`[[7,10],[2,4]]` → `1`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 按开始时间排序，用小根堆（min-heap）存「正在使用的会议室的结束时间」：新会议开始时，如果最早结束的会议已经结束（`堆顶 <= 开始时间`）就复用那间房，否则新开一间；最后堆的大小就是答案。`O(n log n)`。

**识别。** 「区间 + 同时进行的最大数量 / 最少资源」是扫描线（sweep line）或堆的信号。区间题先排序；"要判断最早释放的资源"自然想到小根堆。`n <= 10^4`，`O(n^2)` 两两比较勉强能过，但 `O(n log n)` 才是预期。

**推导。** 暴力：枚举每个时刻统计有多少会议覆盖它，取最大值，时间 `O(时间范围 * n)`，范围到 `10^6` 不可行；或者对每个会议统计与它重叠的会议数，`O(n^2)`。洞察：答案等于同一时刻最多重叠的会议数。按开始时间依次处理，只需要知道"现有房间里最早空出来的是哪间"，小根堆正好 `O(log n)` 回答；堆顶都还没结束，说明所有房间都在用，必须新开。

**简单解法。** 开始记 `+1`、结束记 `-1`，事件排序后累加，累加值的最大值就是答案。

```python
def min_meeting_rooms(intervals: list[list[int]]) -> int:
    events: list[tuple[int, int]] = []
    for start, end in intervals:
        events.append((start, 1))                   # 开始：占一间
        events.append((end, -1))                    # 结束：放一间
    events.sort()                                   # 同一时刻 -1 排在 +1 前：刚结束就开始不多算
    rooms = best = 0
    for _, delta in events:
        rooms += delta
        best = max(best, rooms)
    return best
```

时间 `O(n log n)`，空间 `O(n)`；复杂度与堆解法相同，也可作最终答案，要记住同一时刻结束事件排前面。

最优解：

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

运行：`[[0,30],[5,10],[15,20]]` → `2`；`[[7,10],[2,4]]` → `1`；`[[1,5],[5,9]]` → `1`（端点相接可复用）；`[[1,2]]` → `1`；`[[1,5],[1,5],[1,5]]` → `3`。

**复杂度。** 时间 `O(n log n)`：排序加 `n` 次堆操作；空间 `O(n)`。

**拓展优化。**
- 开始、结束时间分别排序后双指针，不需要堆和元组：
```python
def min_meeting_rooms_two_pointers(intervals: list[list[int]]) -> int:
    starts = sorted(s for s, _ in intervals)
    ends = sorted(e for _, e in intervals)
    rooms = j = 0                                   # j：最早还没释放的结束时间的下标
    for s in starts:
        if ends[j] <= s:
            j += 1                                  # 有会议已结束：复用它的房间
        else:
            rooms += 1                              # 已开始的会议都没结束：新开一间
    return rooms
```
- 时间范围不大（`end <= 10^6`）时用差分数组，不排序，`O(n + T)`：
```python
from itertools import accumulate


def min_meeting_rooms_diff(intervals: list[list[int]]) -> int:
    diff = [0] * (max(e for _, e in intervals) + 2)
    for start, end in intervals:
        diff[start] += 1
        diff[end] -= 1                              # 结束时刻就释放，端点相接不冲突
    return max(accumulate(diff))                    # 前缀和 = 该时刻同时进行的会议数
```

**易错点。**
- 复用条件是 `ends[0] <= start`，写成 `<` 会把"刚好结束就开始"算成冲突：`[[1,5],[5,9]]` 得 `2`，正确是 `1`。
- 必须先按开始时间排序。不排序直接处理 `[[10,20],[0,5],[6,9]]`，得到 `2`，正确是 `1`。
- 堆里存的是结束时间，不是会议本身；复用时要弹出旧的结束时间，换成新会议的结束时间（`heapreplace`）。

**追问。**
- 不只要数量，还要给每个会议分配房间号：堆里存 `(结束时间, 房间号)`，另用一个空闲房间堆。
- 只问一个人能不能参加所有会议（LC 252）：排序后检查相邻会议有没有重叠。

**同模式。** LC 252 会议室、LC 2402 会议室 III、LC 56 合并区间、LC 435 无重叠区间、LC 1094 拼车。
