---
id: tlc-patterns-intervals-sweep-7-problems
node: patterns.intervals-sweep
type: qa
step: 7
---
## Q
**区间与扫描线｜本组用到区间与扫描线的题**

按变形分类，这个题组里哪些题属于区间 / 扫描线？

## A
**排序后合并 / 判重叠**
- LC 56 合并区间
- LC 252 会议室
- LC 435 无重叠区间（高频）
- LC 163 缺失的区间（高频）

**资源数量（事件扫描或堆）**
- LC 253 会议室 II

**差分 / 覆盖计数**

**可达范围是区间的贪心**
- LC 55 跳跃游戏
- LC 45 跳跃游戏 II
- LC 134 加油站（环上的累计量，可看成扫描一遍并在亏空处重置起点）

**区间求交 / 范围约束**
- LC 986 区间列表的交集（高频）

提示：先问端点相接算不算重叠；再决定是「排序后扫描」「事件 +1/-1」还是「排序 + 堆」。

**例题：** LC 56 合并区间

合并所有重叠区间（端点相接也算重叠），返回互不重叠的区间数组；`intervals.length <= 10^4`，端点 `<= 10^4`。

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

**例题：** LC 252 会议室

会议时间 `intervals[i] = [start, end]`，判断一个人能否参加所有会议（首尾相接不算冲突）；`intervals.length <= 10^4`。

```python
from itertools import pairwise
def can_attend_meetings(intervals: list[list[int]]) -> bool:
    ordered = sorted(intervals)
    return all(prev[1] <= cur[0] for prev, cur in pairwise(ordered))
```

**例题：** LC 253 会议室 II

会议时间 `intervals[i] = [start, end]`，一个会议结束的时刻可立刻开始下一个，求最少需要几间会议室；`intervals.length <= 10^4`。

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

**例题：** LC 55 跳跃游戏

`nums[i]` 是在下标 `i` 最多能向前跳的距离，从下标 `0` 出发，判断能否到达最后一个下标；`nums.length <= 10^4`。

```python
def can_jump(nums: list[int]) -> bool:
    reach = 0
    for i, step in enumerate(nums):
        if i > reach:
            return False
        reach = max(reach, i + step)
    return True
```

**例题：** LC 45 跳跃游戏 II

同跳跃游戏，保证能到达最后一个下标，求最少跳跃次数；`nums.length <= 10^4`，`nums[i] <= 1000`。

```python
def jump(nums: list[int]) -> int:
    jumps = cur_end = farthest = 0
    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        if i == cur_end:
            jumps += 1
            cur_end = farthest
    return jumps
```

**例题：** LC 134 加油站

环形路线上 `gas[i]` 是加油量，`cost[i]` 是到下一站的耗油，油箱无限、起始为空；返回能绕一圈的唯一起点，不存在返回 `-1`；`n <= 10^5`。

```python
def can_complete_circuit(gas: list[int], cost: list[int]) -> int:
    total = tank = start = 0
    for i, (g, c) in enumerate(zip(gas, cost)):
        diff = g - c
        total += diff
        tank += diff
        if tank < 0:
            start, tank = i + 1, 0
    return start if total >= 0 else -1
```

**例题：** LC 435 无重叠区间

区间数组 `intervals`，返回最少需要移除多少个区间才能让剩下的两两不重叠（只在端点接触不算重叠）；`1 <= intervals.length <= 10^5`。

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

**例题：** LC 163 缺失的区间

闭区间 `[lower, upper]` 和升序数组 `nums`（元素互不相同且都在区间内），返回恰好覆盖所有缺失数的最小有序区间列表；`0 <= nums.length <= 100`，`-10^9 <= lower <= upper <= 10^9`。

```python
from itertools import chain
def find_missing_ranges(nums: list[int], lower: int, upper: int) -> list[list[int]]:
    ans: list[list[int]] = []
    prev = lower - 1
    for x in chain(nums, (upper + 1,)):
        if x - prev >= 2:
            ans.append([prev + 1, x - 1])
        prev = x
    return ans
```

**例题：** LC 986 区间列表的交集

两个已排序、列表内两两不相交的闭区间列表 `firstList`、`secondList`，返回它们的交集；每个列表长度 `<= 1000`。

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
