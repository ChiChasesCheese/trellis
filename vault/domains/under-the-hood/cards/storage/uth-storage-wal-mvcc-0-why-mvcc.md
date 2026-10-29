---
id: uth-storage-wal-mvcc-0-why-mvcc
node: storage.wal-mvcc
type: qa
step: 2
---
## Q
**MVCC：读不等写，靠保留多个版本**｜PostgreSQL · 18 / InnoDB · MySQL 8.4

一个事务正在改某一行，另一个事务同时要读这一行：读的人要等写的人吗？

## A
**背景。** 最直接的办法是加锁：写的时候，读的人排队等。数据库一忙，读和写就互相卡住。

**结构。** 多版本并发控制（MVCC）：改一行不覆盖旧值，而是另存一个新版本，每个版本记着是哪个事务写的。读事务开始时拿一个快照（它开始那一刻“哪些事务已提交”的记录），读的时候只认快照之前已经提交的版本。图里事务 105 把余额从 50 改成 80：开始于 103 的读者仍然读到 50，开始于 106 的读者读到 80，谁也不用等谁。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 142">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同一行的两个版本 (余额)</text>
<text x="100" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">事务 100 写入</text>
<text x="240" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">事务 105 写入</text>
<rect x="60" y="48" width="80" height="30" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="100" y="67.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">v1: 50</text>
<rect x="200" y="48" width="80" height="30" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="240" y="67.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">v2: 80</text>
<line x1="140" y1="66" x2="194" y2="66" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="200,66 194.0,69.0 194.0,63.0" stroke="currentColor" stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="60" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">被取代</text>
<line x1="100" y1="118" x2="100" y2="86" stroke="currentColor" stroke-width="1.2"/>
<polygon points="100,80 103.0,86.0 97.0,86.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="240" y1="118" x2="240" y2="86" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="240,80 243.0,86.0 237.0,86.0" stroke="currentColor" stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<text x="100" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读者 X 开始于 103</text>
<text x="240" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读者 Y 开始于 106</text>
</svg>
```

**为什么。** 读不阻塞写、写不阻塞读；代价是旧版本要占地方，没人需要时还得清理。

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
