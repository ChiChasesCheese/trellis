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

**资源数量（事件扫描或堆）**
- LC 253 会议室 II
- LC 2402 会议室 III（房间号堆 + 结束时间堆）

**差分 / 覆盖计数**
- LC 2021 街上最亮的位置

**可达范围是区间的贪心**
- LC 55 跳跃游戏
- LC 45 跳跃游戏 II
- LC 134 加油站（环上的累计量，可看成扫描一遍并在亏空处重置起点）

**区间求交 / 范围约束**
- LC 2145 统计隐藏数组数目（起点必须落在由前缀最值得出的区间内）

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

**例题：** LC 2402 会议室 III

`n` 个会议室，会议按开始时间依次分配到编号最小的空闲房间，没有空房就延期到最早空出时开始（时长不变），求举办次数最多的房间（并列取编号小）；`n <= 100`，`meetings.length <= 10^5`，`start` 互不相同。

```python
from heapq import heappop, heappush
def most_booked(n: int, meetings: list[list[int]]) -> int:
    free = list(range(n))
    busy: list[tuple[int, int]] = []
    count = [0] * n
    for start, end in sorted(meetings):
        while busy and busy[0][0] <= start:
            heappush(free, heappop(busy)[1])
        if free:
            room = heappop(free)
            finish = end
        else:
            ready, room = heappop(busy)
            finish = ready + (end - start)
        count[room] += 1
        heappush(busy, (finish, room))
    return max(range(n), key=count.__getitem__)
```

**例题：** LC 2021 街上最亮的位置

路灯 `[position, range]` 照亮闭区间 `[position - range, position + range]`，求被最多路灯照到的位置（并列取最小）；`lights.length <= 10^5`，坐标绝对值 `<= 10^8`。

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

**例题：** LC 2145 统计隐藏数组数目

已知隐藏数组相邻元素的差 `differences`，且所有元素都在 `[lower, upper]` 内，求可能的隐藏数组个数；`differences.length <= 10^5`。

```python
from itertools import accumulate
def number_of_arrays(differences: list[int], lower: int, upper: int) -> int:
    prefix = [0, *accumulate(differences)]
    spread = max(prefix) - min(prefix)
    return max(0, (upper - lower) - spread + 1)
```
