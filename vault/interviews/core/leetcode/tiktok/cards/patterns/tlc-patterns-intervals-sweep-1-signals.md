---
id: tlc-patterns-intervals-sweep-1-signals
node: patterns.intervals-sweep
type: qa
step: 1
---
## Q
**区间与扫描线（Intervals / Sweep Line）｜信号**

什么样的题面该想到「排序后扫描」「扫描线」或「差分」？哪些近似信号需要别的方法？

## A
**信号：**
- 输入是一组 `[start, end]` 区间，问**合并**、**是否重叠**（例：LC 56 合并区间）。
- 「某个点被几个区间覆盖」「最亮的位置」：把每个区间拆成 `+1`（开始）和 `-1`（结束）两个事件，排序后累加（例：LC 2021 街上最亮的位置）。
- 「按时间顺序处理事件，每个事件需要最早空闲的资源」，问**最多同时有几个**、**需要几个资源**：排序 + 堆（例：LC 253 会议室 II）。
- 「用最少的区间覆盖 / 选最多互不重叠的区间」：按右端点（结束时间）排序的贪心（例：LC 435 无重叠区间）。
- 「跳跃能到达的范围」：可达范围是一个区间，向右延伸（例：LC 55 跳跃游戏）。

**核心思路**：**先排序，让相关的区间相邻**；排序之后，重叠只可能发生在相邻（或与当前最右端）之间，一次扫描 `O(n)`，总共 `O(n log n)`。

**近似信号：**
- 区间非常多、坐标范围小（`<= 10^6`）→ 差分数组，不必排序（例：LC 1094 拼车）。
- 要**动态**插入、删除区间并查询 → 平衡树 / 线段树，不是一次排序；只插入一次，线性扫描就够（例：LC 57 插入区间）。
- 区间是二维的（矩形）→ 扫描线 + 线段树（复杂得多）。
- 只问两个有序区间列表的交集 → 双指针比较 `max(起点)` 与 `min(终点)`，不需要重新排序（例：LC 986 区间列表的交集）。
- **端点相接**算不算重叠，是每道题的第一个澄清问题（例：LC 252 会议室）。

**例题：** LC 56 合并区间

合并所有重叠的区间并返回不重叠的区间数组，`1 <= intervals.length <= 10^4`，`0 <= start <= end <= 10^4`。

```python
def merge(intervals: list[list[int]]) -> list[list[int]]:
    merged: list[list[int]] = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged
```

**例题：** LC 2021 街上最亮的位置

路灯 `[position, range]` 照亮闭区间 `[position - range, position + range]`，返回被最多路灯照亮的位置，并列取最小，`1 <= lights.length <= 10^5`，`-10^8 <= position <= 10^8`。

```python
from collections import defaultdict
def brightest_position(lights: list[list[int]]) -> int:
    diff: defaultdict[int, int] = defaultdict(int)
    for pos, rng in lights:
        diff[pos - rng] += 1
        diff[pos + rng + 1] -= 1
    best = cur = 0
    ans = 0
    for x in sorted(diff):
        cur += diff[x]
        if cur > best:
            best, ans = cur, x
    return ans
```

**例题：** LC 253 会议室 II

给定会议时间 `[start, end]`，返回所需会议室的最小数量，`1 <= intervals.length <= 10^4`，`0 <= start < end <= 10^6`。

```python
import heapq
def min_meeting_rooms(intervals: list[list[int]]) -> int:
    ends: list[int] = []
    for start, end in sorted(intervals):
        if ends and ends[0] <= start:
            heapq.heapreplace(ends, end)
        else:
            heapq.heappush(ends, end)
    return len(ends)
```

**例题：** LC 435 无重叠区间

返回需要移除的最少区间数，使剩下的区间互不重叠；只在一点接触的区间不算重叠，`1 <= intervals.length <= 10^5`。

```python
from math import inf
from operator import itemgetter
def erase_overlap_intervals(intervals: list[list[int]]) -> int:
    kept, end = 0, -inf
    for start, finish in sorted(intervals, key=itemgetter(1)):
        if start >= end:
            kept += 1
            end = finish
    return len(intervals) - kept
```

**例题：** LC 55 跳跃游戏

`nums[i]` 是从下标 `i` 最多能跳的步数，判断能否从下标 0 到达最后一个下标，`1 <= nums.length <= 10^4`。

```python
def can_jump(nums: list[int]) -> bool:
    reach = 0
    for i, step in enumerate(nums):
        if i > reach:
            return False
        reach = max(reach, i + step)
    return True
```

**例题：** LC 1094 拼车

车有 `capacity` 个座位且不能掉头，`trips[i] = [人数, 上车里程, 下车里程]`，同一位置先下后上；判断是否任意一点都不超载，`1 <= trips.length <= 1000`，里程 `<= 1000`。

```python
def car_pooling(trips: list[list[int]], capacity: int) -> bool:
    change = [0] * 1001
    for passengers, start, end in trips:
        change[start] += passengers
        change[end] -= passengers
    current = 0
    for delta in change:
        current += delta
        if current > capacity:
            return False
    return True
```

**例题：** LC 57 插入区间

给互不重叠且按起点升序的区间列表和一个新区间，插入并合并后返回，`0 <= intervals.length <= 10^4`。

```python
def insert(intervals: list[list[int]], new_interval: list[int]) -> list[list[int]]:
    result: list[list[int]] = []
    start, end = new_interval
    i, n = 0, len(intervals)
    while i < n and intervals[i][1] < start:
        result.append(intervals[i])
        i += 1
    while i < n and intervals[i][0] <= end:
        start = min(start, intervals[i][0])
        end = max(end, intervals[i][1])
        i += 1
    result.append([start, end])
    while i < n:
        result.append(intervals[i])
        i += 1
    return result
```

**例题：** LC 986 区间列表的交集

两个各自内部不相交且已排序的闭区间列表，返回它们的交集，每个列表长度 `<= 1000`。

```python
def interval_intersection(first: list[list[int]], second: list[list[int]]) -> list[list[int]]:
    i = j = 0
    ans: list[list[int]] = []
    while i < len(first) and j < len(second):
        lo = max(first[i][0], second[j][0])
        hi = min(first[i][1], second[j][1])
        if lo <= hi:
            ans.append([lo, hi])
        if first[i][1] < second[j][1]:
            i += 1
        else:
            j += 1
    return ans
```

**例题：** LC 252 会议室

判断一个人能否参加所有会议（在 `t` 结束的会议和在 `t` 开始的会议不重叠），`0 <= intervals.length <= 10^4`。

```python
from itertools import pairwise
def can_attend_meetings(intervals: list[list[int]]) -> bool:
    ordered = sorted(intervals)
    return all(prev[1] <= cur[0] for prev, cur in pairwise(ordered))
```
