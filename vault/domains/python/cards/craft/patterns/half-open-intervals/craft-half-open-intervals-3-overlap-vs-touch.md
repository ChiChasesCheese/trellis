---
id: craft-half-open-intervals-3-overlap-vs-touch
node: craft.patterns.half-open-intervals
type: qa
step: 3
---
## Q
**半开区间 · 判断「重叠」和判断「挨得上」只差一个等号，为什么两者都需要**｜模式

会议调度：`10:00–11:00` 和 `11:00–12:00` 能同时安排给一个人吗？找一群人的共同空档时，先要把每个人忙碌的区间合并，这两个区间该不该合并成 `10:00–12:00`？空区间（开始等于结束）能不能存在？

## A
**要点。** 两个问题的答案不同，但都来自同一个半开约定。**冲突判断**用严格小于：`a.start < b.end and b.start < a.end`，首尾相接不冲突。**合并**用小于等于：下一个区间的起点 `<=` 当前区间的终点就并进去（"挨得上或重叠"），因为合并之后的忙碌时间是连续的；合并是为了找空档，若不把相邻的合并，会在两个相邻区间之间"看到一道缝"，缝的长度是 0，但会被当成一个可用的空档。空区间 `[3, 3)` 在构造时就拒绝：它不占用任何时间，却会被重叠判断说成与 `[1, 5)` 冲突。

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Interval:
    start: int; end: int
    def __post_init__(self):
        if self.end <= self.start: raise ValueError(f"end {self.end} must be after start {self.start}")
    def overlaps(self, o): return self.start < o.end and o.start < self.end       # 严格小于

def merge(intervals):
    out = []
    for iv in sorted(intervals, key=lambda i: i.start):
        if out and iv.start <= out[-1].end:                                       # 挨得上也并：<=
            out[-1] = Interval(out[-1].start, max(out[-1].end, iv.end))
        else: out.append(iv)
    return out

a, b = Interval(10, 11), Interval(11, 12)
print("10-11 与 11-12 重叠?", a.overlaps(b), " 合并后:", merge([a, b]))
try: Interval(3, 3)
except ValueError as e: print("空区间:", e)

class Raw:                                         # 为什么空区间要拒绝：假如允许构造 [3, 3)
    def __init__(s, a, b): s.start, s.end = a, b
    def overlaps(s, o): return s.start < o.end and o.start < s.end
print("若允许 [3,3) :", Raw(3, 3).overlaps(Raw(1, 5)), "，空区间却与别人冲突")
```

```
10-11 与 11-12 重叠? False  合并后: [Interval(start=10, end=12)]
空区间: end 3 must be after start 3
若允许 [3,3) : True ，空区间却与别人冲突
```

**为什么。** 把"区间的合法性"放进构造（`__post_init__` 里 `end > start`），非法区间就造不出来，下游的每个函数都不必再考虑零长度这个特例。合并时用 `max(out[-1].end, iv.end)` 而不是直接取 `iv.end`：后一个区间可能被前一个完全包住。

**易错。** 合并之前必须按起点排序；两个人各占忙碌的一部分、且彼此挨着时，不先合并就会误判中间有缝。

**对照。** LeetCode Meeting Rooms：按开始时间排序后，`prev[1] <= cur[0]` 才算不冲突，注意 `<=`：结束时刻等于下一个的开始时刻，在半开约定下不冲突。
