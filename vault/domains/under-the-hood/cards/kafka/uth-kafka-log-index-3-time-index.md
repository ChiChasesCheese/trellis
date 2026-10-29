---
id: uth-kafka-log-index-3-time-index
node: kafka.log-index
type: qa
step: 3
---
## Q
**按时间找消息：时间索引与预分配**｜Kafka · 4.0

按时间戳查消息（`offsetsForTimes`）怎样串起两个索引？为什么活动段的 `.index` 文件大小永远是 10485760 字节？

## A
**背景。** 前面的索引只能“偏移量 → 文件位置”。按时间查，需要先把时间换成偏移量。

**结构。** `.timeindex` 是第二张稀疏索引，每项 12 字节（8 字节时间戳 + 4 字节相对偏移），和 `.index` 同时追加。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 184">
<text x="170" y="14" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">目标时间 T</text>
<line x1="170" y1="20" x2="170" y2="26" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,32 167.0,26.0 173.0,26.0" stroke="currentColor" stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<rect x="12" y="32" width="316" height="32" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="170" y="52.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">.timeindex  时间戳 -&gt; 偏移量 (12 字节/项)</text>
<line x1="170" y1="64" x2="170" y2="82" stroke="currentColor" stroke-width="1.2"/>
<polygon points="170,88 167.0,82.0 173.0,82.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="180" y="82" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">二分: 不晚于 T 的最后一项</text>
<rect x="12" y="88" width="316" height="32" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="108.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">.index  偏移量 -&gt; 文件位置 (8 字节/项)</text>
<line x1="170" y1="120" x2="170" y2="138" stroke="currentColor" stroke-width="1.2"/>
<polygon points="170,144 167.0,138.0 173.0,138.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="180" y="138" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">二分: 不大于它的最后一项</text>
<rect x="12" y="144" width="316" height="32" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="164.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">.log  从该位置起顺序扫</text>
</svg>
```

**细节。**

- 先在 `.timeindex` 二分出不晚于目标时间的偏移量，再用 `.index` 换成文件位置，最后顺序扫 `.log`。
- 索引文件新建时就按 `segment.index.bytes`（10 MiB）预分配（一次占好整个大小），向下取整到项大小的整数倍：`.index` 是 10485760，`.timeindex` 是 10485756；段滚动时才截成实际大小。

**为什么。** 预分配的内存映射文件追加写入不用扩文件；代价是 `ls` 看到的大小不是真实用量。

**例题：** LC 981 基于时间的键值存储

设计 `TimeMap`：`set(key, value, timestamp)` 存入；`get(key, timestamp)` 返回此前某次 `set` 中时间戳不大于 `timestamp` 的最大者对应的值，没有则返回空串。所有 `set` 的时间戳严格递增。例：`set("foo","bar",1)`；`get("foo",3)` → `"bar"`；`set("foo","bar2",4)`；`get("foo",5)` → `"bar2"`。

```python
from bisect import bisect_right
from collections import defaultdict


class TimeMap:
    def __init__(self) -> None:
        self.times: defaultdict[str, list[int]] = defaultdict(list)    # key -> 递增的时间戳
        self.values: defaultdict[str, list[str]] = defaultdict(list)   # key -> 与 times 同下标的值

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.times[key].append(timestamp)       # 时间戳严格递增：直接 append 就是有序的
        self.values[key].append(value)

    def get(self, key: str, timestamp: int) -> str:
        times = self.times.get(key)             # 用 .get：defaultdict 的 [] 会凭空造出空列表
        if not times:
            return ""
        i = bisect_right(times, timestamp)      # 第一个 > timestamp 的位置，i-1 就是最后一个 <= timestamp 的
        return self.values[key][i - 1] if i else ""
```
