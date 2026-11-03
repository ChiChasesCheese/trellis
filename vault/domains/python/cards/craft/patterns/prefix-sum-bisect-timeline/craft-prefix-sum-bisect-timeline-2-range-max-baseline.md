---
id: craft-prefix-sum-bisect-timeline-2-range-max-baseline
node: craft.patterns.prefix-sum-bisect-timeline
type: qa
step: 2
---
## Q
**前缀和时间线 · 「一段时间内最多有多少人」为什么不能只看区间内的事件**｜模式

在上一张卡的时间线上，要回答「[a, b] 这段时间里楼里最多出现过多少人」。直觉的写法是取出时间落在 [a, b] 里的事件，在它们的 `counts` 里取最大。查询 [11, 11]（这一秒没有事件）会得到什么？

## A
**要点。** 区间开始时楼里**已经有人**，这个基线不是区间内任何事件产生的。只看区间内的事件，区间里没有事件时得到 0，区间里有事件时也可能漏掉比这些事件更大的开头值。正确答案 = max(区间开始时的人数，区间内每个事件之后的人数)。

```python
import bisect

class Timeline:
    def __init__(self): self.times, self.counts = [], []
    def append(self, ts, delta):
        self.times.append(ts)
        self.counts.append((self.counts[-1] if self.counts else 0) + delta)
    def count_at(self, ts):
        i = bisect.bisect_right(self.times, ts) - 1
        return self.counts[i] if i >= 0 else 0

def max_in_wrong(tl, a, b):                               # 只看区间里的事件
    lo, hi = bisect.bisect_left(tl.times, a), bisect.bisect_right(tl.times, b)
    return max(tl.counts[lo:hi], default=0)

def max_in(tl, a, b):
    lo = bisect.bisect_left(tl.times, a)       # 第一个 time >= a
    hi = bisect.bisect_right(tl.times, b)      # 第一个 time > b
    return max([tl.count_at(a), *tl.counts[lo:hi]])   # 区间开始时的人数也要算

tl = Timeline()
for ts, d in [(9, +1), (10, +1), (12, -1), (15, +1), (15, +1), (18, -1)]:
    tl.append(ts, d)
for a, b in [(10, 11), (11, 11), (13, 14), (12, 15)]:
    print(f"[{a},{b}]  只看区间内事件: {max_in_wrong(tl, a, b)}  加上区间开始时的人数: {max_in(tl, a, b)}")
```

用同一组事件：

```
[10,11]  只看区间内事件: 2  加上区间开始时的人数: 2
[11,11]  只看区间内事件: 0  加上区间开始时的人数: 2
[13,14]  只看区间内事件: 0  加上区间开始时的人数: 1
[12,15]  只看区间内事件: 3  加上区间开始时的人数: 3
```

**为什么。** 前缀和是「状态」，事件只是状态变化的时刻；状态在两个事件之间保持不变。所以一个区间内的最大值，由「进入区间时的状态」和「区间内每次变化后的状态」共同决定。这是所有"状态随事件变化"问题的共同陷阱：区间的开头要先取一个基线。

**怎么加速。** 上面的切片取最大是 O(区间内事件数)。追加型数据可以配一棵只追加的线段树存 `counts` 的区间最大值，查询 O(log n)；追加时容量翻倍重建，摊还 O(1)。事件少的时候直接切片就够，别过早引入线段树。

**易错。** `bisect_left` 对起点、`bisect_right` 对终点，保证区间是**闭区间** `[a, b]`：起止点上正好有事件的情形都被包含；用错一边，边界事件会被漏掉。
