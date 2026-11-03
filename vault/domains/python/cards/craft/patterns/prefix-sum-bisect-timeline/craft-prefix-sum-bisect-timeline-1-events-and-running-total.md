---
id: craft-prefix-sum-bisect-timeline-1-events-and-running-total
node: craft.patterns.prefix-sum-bisect-timeline
type: qa
step: 1
---
## Q
**前缀和时间线 · 「某个历史时刻楼里有多少人」该怎么存**｜写法

办公室每次有人进出就产生一条事件（时间，+1 或 -1）。要回答「上午 11 点楼里有几个人」。只维护一个「当前人数」计数器可以吗？不可以的话，该存什么、怎么查？

## A
**要点。** 当前人数只能回答现在。要回答历史，就存事件，并把**前缀和**（prefix sum，到第 i 个事件为止的累计值）和事件时间并排存成两个数组：`times[i]` 是第 i 个事件的时间，`counts[i]` 是处理完它之后的人数。查询 t 时刻，用 `bisect_right(times, t) - 1` 找到最后一个时间 `<= t` 的事件，答案就是它对应的 `counts`；找不到（t 比所有事件都早）答案是 0。写入是 O(1) 追加，查询是 O(log n)。

```python
import bisect

class Timeline:
    """只追加：times[i] 是第 i 个事件的时间，counts[i] 是处理完它之后的人数（前缀和）。"""
    def __init__(self): self.times, self.counts = [], []
    def append(self, ts, delta):
        self.times.append(ts)
        self.counts.append((self.counts[-1] if self.counts else 0) + delta)
    def count_at(self, ts):
        i = bisect.bisect_right(self.times, ts) - 1       # 最后一个 time <= ts 的事件
        return self.counts[i] if i >= 0 else 0            # 还没有任何事件：0

tl = Timeline()
for ts, d in [(9, +1), (10, +1), (12, -1), (15, +1), (15, +1), (18, -1)]:
    tl.append(ts, d)
print("counts =", tl.counts)
for t in (8, 9, 11, 15, 100):
    print(f"count_at({t:3}) = {tl.count_at(t)}")
```

事件 (9,+1)(10,+1)(12,-1)(15,+1)(15,+1)(18,-1)：

```
counts = [1, 2, 1, 2, 3, 2]
count_at(  8) = 0
count_at(  9) = 1
count_at( 11) = 2
count_at( 15) = 3
count_at(100) = 2
```

**为什么。** `bisect_right`：同一时刻有多个事件时（15 秒有两个），要取**最后一个**的前缀和，因为查询 t 的语义是「t 这一秒结束时」；用 `bisect_left` 会漏掉同一时刻的后续事件。`i >= 0` 的判断不能省，`counts[-1]` 在 Python 里是合法的，会悄悄返回最后一项。

**前提。** 事件必须按时间不递减地追加：前缀和只能追加，不能在中间插入（插入会让后面所有前缀和失效）。所以倒流的事件被拒绝，同一个人的重复重试事件被忽略。

**代价。** 内存与事件数成正比，且只增不减；事件很多时要靠检查点或归档，而不是删除。
