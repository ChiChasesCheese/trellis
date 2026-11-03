---
id: craft-derived-not-stored-3-copies-go-stale
node: craft.patterns.derived-not-stored
type: qa
step: 3
---
## Q
**派生而非存储 · 旅客行程里要不要抄一份座位号**｜写法

航班订座里，旅客行程由若干「航段」组成。每个航段记录「他在某一班上占的舱位」。想知道某位旅客的座位号，最直接的是在航段里存一个 `seat` 字段。旅客改签到另一班以后会发生什么？

## A
**要点。** 座位属于**那一班航班**的座位图（座位 → 持有者）。航段里再抄一份座位号，就是一个会过期的副本：改签换班之后，航段指向新航班，抄来的座位号却还是旧班的。正确做法是航段不存座位，需要时去航班的座位图里查：`next(label for label, holder in seats.items() if holder == ref)`。

```python
from dataclasses import dataclass

class Flight:
    def __init__(self, name): self.name, self.seats = name, {}     # 座位图：座位 -> 持有者

@dataclass
class StoredSegment:                      # 把座位号抄了一份在行程里
    flight: Flight; seat: str | None = None

@dataclass(frozen=True)
class Segment:                            # 座位属于那一班的座位图，这里只有"哪一班"
    flight: Flight
    def seat_of(self, ref):
        return next((s for s, holder in self.flight.seats.items() if holder == ref), None)

a, b = Flight("MU100"), Flight("MU200")
a.seats["12A"] = "ref1"
stored, derived = StoredSegment(a, "12A"), Segment(a)
del a.seats["12A"]; stored.flight = b; derived = Segment(b)       # 改签：换到 MU200，旧班座位释放
print("抄存的座位号:", stored.seat, "<- 过期副本，MU200 上并没有这个座位")
print("算出来的座位号:", derived.seat_of("ref1"))
```

旅客从 MU100（12A）改签到 MU200：

```
抄存的座位号: 12A <- 过期副本，MU200 上并没有这个座位
算出来的座位号: None
```

**为什么。** 「该存在哪儿」的判据是**所有权**：一个事实只归一个地方管（座位归航班，位置归行程表，起飞时间归状态轨迹）。其他地方要用，就通过引用去查。`ride-sharing` 里 `started_at` 也是直接从状态轨迹里读（第一次进入 `IN_PROGRESS` 的那条记录），不另存字段，所以没有两份真相。

**代价。** 查要多一次查找；座位图很大时要建反向索引（持有者 → 座位）。反向索引就是一个必须与主表同步的派生结构，所以要小心：只在写入的同一个临界区里更新它，并在测试里断言它与现算结果相等。

**对照。** 数据库的范式化（normalization）是同一个原则：不存可以由别的列算出来的列。
