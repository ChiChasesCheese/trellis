---
id: uth-kafka-timing-wheel-2-no-tick
node: kafka.timing-wheel
type: qa
step: 2
---
## Q
**时间轮不需要每毫秒滴答**｜Kafka · 4.0

最细的一层每格只有 1 ms，难道有个线程每毫秒转一格？

## A
**背景。** 如果真有线程每毫秒醒一次，系统空闲时也在白白消耗 CPU。

**结构。** 不是这样。每个非空的格（bucket）被放进一个 `DelayQueue`（按到期时间排序、没到期就取不出来的队列）；线程用 `poll` 阻塞到最早的格到期，再把时钟直接推进到那一格的起点。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 162">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">时间轮的格 (灰色 = 非空)</text>
<rect x="26" y="20" width="24" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="50" y="20" width="24" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="74" y="20" width="24" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="98" y="20" width="24" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="122" y="20" width="24" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="146" y="20" width="24" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="170" y="20" width="24" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="194" y="20" width="24" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="218" y="20" width="24" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="242" y="20" width="24" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="266" y="20" width="24" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="290" y="20" width="24" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="40" y="84" width="56" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="68" y="101.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t=2</text>
<line x1="62" y1="42" x2="68" y2="84" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<rect x="110" y="84" width="56" height="26" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="138" y="101.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t=5</text>
<line x1="134" y1="42" x2="138" y2="84" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<rect x="180" y="84" width="56" height="26" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="208" y="101.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t=6</text>
<line x1="158" y1="42" x2="208" y2="84" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<rect x="250" y="84" width="56" height="26" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="278" y="101.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t=10</text>
<line x1="254" y1="42" x2="278" y2="84" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="68" y1="112" x2="68" y2="118" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="68,124 65.0,118.0 71.0,118.0" stroke="currentColor" stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<text x="78" y="134" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">poll 睡到最早的格到期</text>
<text x="8" y="154" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">DelayQueue: 按到期时间排序</text>
</svg>
```

**细节。**

- `DelayQueue` 里装的是格，不是任务，元素个数不超过格数。
- 取出到期的格后 `flush`：把里面的任务逐个重新 `add`，已到期的直接执行，来自高层的落进更细的层。

**为什么。** 推进时间的代价取决于非空格的个数，而不是任务总数；系统空闲时线程就睡着。

**例题：** LC 253 会议室 II

给会议时间数组 `intervals[i] = [start, end]`，返回同时容纳所有会议所需的最少会议室数；一个会议结束的时刻可以立刻开始下一个。`1 <= intervals.length <= 10^4`。例：`[[0,30],[5,10],[15,20]]` → `2`。

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
