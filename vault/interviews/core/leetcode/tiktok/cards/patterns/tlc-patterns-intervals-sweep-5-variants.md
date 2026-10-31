---
id: tlc-patterns-intervals-sweep-5-variants
node: patterns.intervals-sweep
type: qa
step: 5
---
## Q
**区间与扫描线｜变形：两个区间表求交、跳跃游戏的可达范围、区间上的覆盖计数**

除了合并和会议室，区间题还有哪些常见形态？各自的扫描方式是什么？

## A
1. **两个已排序的区间表求交集**（双指针，每次推进右端点更小的那个）（例：LC 986 区间列表的交集）。输入 `[[0,2],[5,10],[13,23],[24,25]]` 与 `[[1,5],[8,12],[15,24],[25,26]]` 得 `[[1,2],[5,5],[8,10],[15,23],[24,24],[25,25]]`。

2. **可达范围是区间**：维护「当前能到达的最远下标」`far`；若某个下标 `i > far`，说明走不到（例：LC 55 跳跃游戏）。`[2,3,1,1,4]` 得 `True`，`[3,2,1,0,4]` 得 `False`。LC 45 跳跃游戏 II 是同一个思路加「分层」：当前这一跳能到的区间 `[lo, hi]`，扫完这一层就跳数 +1。

3. **区间上的覆盖计数**：每个区间在起点 `+1`、终点之后 `-1` 记成差分，累加得到每处的覆盖数；坐标很大时用字典记差分、只对出现过的端点排序；见前缀和与差分一组（例：LC 1094 拼车）。

4. **资源调度（LC 253）**：排序 + 堆，见堆一组（例：LC 253 会议室 II）。

5. **选最多互不重叠区间 / 最少箭射爆气球**：按**右端点**排序，贪心选结束最早的；与合并按左端点排序不同（例：LC 435 无重叠区间）。

**例题：** LC 986 区间列表的交集

给两个由**闭区间**组成的列表 `firstList` 和 `secondList`，每个列表内部的区间两两不相交且已按起点排序。返回这两个列表的交集（同样是一组闭区间）。闭区间 `[a, b]` 表示实数 `a <= x <= b`，两个闭区间的交集要么为空，要么是闭区间，例如 `[1,3]` 和 `[2,4]` 的交集是 `[2,3]`。`0 <= firstList.length, secondList.length <= 1000`，两者长度之和 `>= 1`，`0 <= start < end <= 10^9`，同一列表中 `end_i < start_{i+1}`。

```python
def interval_intersection(first: list[list[int]], second: list[list[int]]) -> list[list[int]]:
    i = j = 0
    ans: list[list[int]] = []
    while i < len(first) and j < len(second):
        lo = max(first[i][0], second[j][0])      # 交集左端取较大的起点
        hi = min(first[i][1], second[j][1])      # 右端取较小的终点
        if lo <= hi:                             # 闭区间：lo == hi 也是一个点
            ans.append([lo, hi])
        if first[i][1] < second[j][1]:           # 终点小的那个不可能再与对方后面的区间相交
            i += 1
        else:
            j += 1
    return ans
```

**例题：** LC 55 跳跃游戏

给非负整数数组 `nums`，你最初位于第一个下标，数组中每个元素是你在该位置**最多**可以向前跳的长度。判断能否到达最后一个下标。`1 <= nums.length <= 10^4`，`0 <= nums[i] <= 10^5`。

```python
def can_jump(nums: list[int]) -> bool:
    reach = 0                               # 目前能到达的最远下标
    for i, step in enumerate(nums):
        if i > reach:
            return False                    # 连 i 都够不着，后面更不可能
        reach = max(reach, i + step)
    return True
```

**例题：** LC 1094 拼车

车有 `capacity` 个座位且只能往一个方向开；`trips[i] = [人数, 上车里程, 下车里程]`，同一位置先下后上。判断途中任意一点是否都不超载。`1 <= trips.length <= 1000`，`0 <= from < to <= 1000`，`1 <= capacity <= 10^5`。

```python
def car_pooling(trips: list[list[int]], capacity: int) -> bool:
    change = [0] * 1001  # 里程 0..1000 上的人数变化量
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

**例题：** LC 253 会议室 II

给一个会议时间数组 `intervals`，`intervals[i] = [start_i, end_i]`，返回需要的最少会议室数量。一个会议结束的时刻可以立刻开始下一个会议。`1 <= intervals.length <= 10^4`，`0 <= start_i < end_i <= 10^6`。

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

**例题：** LC 435 无重叠区间

给一组区间 `intervals`，`intervals[i] = [start_i, end_i]`。返回最少需要移除多少个区间，才能让剩下的区间两两不重叠。只在端点接触的区间不算重叠，例如 `[1,2]` 和 `[2,3]`。`1 <= intervals.length <= 10^5`，`intervals[i].length == 2`，`-5 * 10^4 <= start_i < end_i <= 5 * 10^4`。

```python
from math import inf
from operator import itemgetter


def erase_overlap_intervals(intervals: list[list[int]]) -> int:
    kept, end = 0, -inf                                   # 已保留的区间数、最后保留区间的右端点
    for start, finish in sorted(intervals, key=itemgetter(1)):   # 按右端点升序
        if start >= end:                                  # 只在端点接触不算重叠，所以是 >=
            kept += 1
            end = finish
    return len(intervals) - kept
```
