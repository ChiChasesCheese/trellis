---
id: craft-observability-as-design-3-metrics-are-frozen-snapshots
node: craft.architecture.observability-as-design
type: qa
step: 3
---
## Q
**可观测性即设计 · 缓存的命中统计为什么返回冻结快照，而不是直接暴露内部计数器**｜架构

缓存要提供命中、未命中、驱逐次数。最省事的做法是把内部的计数器直接交给调用方。并发的缓存里，这样做会让监控代码读到什么？

## A
**要点。** 对外只给一个**冻结的快照**（frozen snapshot）：在锁内一次读完所有计数，装进不可变对象再交出去。TTL 缓存的 `CacheStats` 和熔断器的 `Metrics` 都是这样做的，注释同样写明：不可变，所以拿到之后读到的数字不会自己变。

```python
from dataclasses import dataclass, FrozenInstanceError

@dataclass(frozen=True, slots=True)
class Stats:                               # 某一瞬间的快照
    hits: int
    misses: int
    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total else 0.0

import threading

class Cache:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._counts = [0, 0]              # 内部计数器：[hits, misses]
    def record(self, hit: bool) -> None:
        with self._lock:
            self._counts[0 if hit else 1] += 1
    def live(self) -> list[int]:           # 直接交出内部对象
        return self._counts
    def stats(self) -> Stats:              # 锁内一次读完，两个数同属一个时刻
        with self._lock:
            return Stats(*self._counts)

c = Cache()
c.record(True); c.record(False)
live, snap = c.live(), c.stats()
c.record(True); c.record(True)             # 之后又来了两次命中
print("live  ", live, "（读到的数字自己变了）")
print("snap  ", snap, "hit_rate =", round(snap.hit_rate, 2))
print("再取  ", c.stats().hit_rate)
try:
    snap.hits = 99
except FrozenInstanceError as e:
    print("改快照:", type(e).__name__)
```

实际输出：

```
live   [3, 1] （读到的数字自己变了）
snap   Stats(hits=1, misses=1) hit_rate = 0.5
再取   0.75
改快照: FrozenInstanceError
```

**为什么。** 直接交出内部对象有两个问题：数字在调用方手里悄悄变化，算 `hit_rate` 时分子和分母可能来自不同时刻；调用方还能顺手改它。快照在锁内一次读完，`hits` 和 `misses` 一定同属一刻，比率才可信。

**代价。** 每次读都会分配一个小对象；监控读取的频率很低，这点开销可以忽略。派生量（`hit_rate`）放在快照上现算，不单独维护，避免与原始计数不一致。
