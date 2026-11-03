---
id: craft-append-only-log-derived-state-1-facts-not-totals
node: craft.patterns.append-only-log-derived-state
type: qa
step: 1
---
## Q
**只追加日志 + 派生状态 · 为什么存事实而不是存累加后的总数**｜模式

配送员按取餐到送达的时长计费。直接的写法：送达时把这单的钱加进应付总额。后来发现一单的送达时间要更正。累加进总额的写法会遇到什么？只存事实又是怎么避开的？

## A
**要点。** 乱序、重复、更正是现实世界的常态。把钱累加进余额，更正时就要先减去旧账、再加新账，而旧账是怎么算的，已经没有记录。只存事实（每单的时间点），钱每次现算，更正只是覆盖一个事实，总额自动跟着对。

```python
# 配送员按「取餐 -> 送达」的时长计费：每分钟 30 分，送达时间稍后可能被更正
RATE = 30

class AccumulatedPay:
    def __init__(self) -> None:
        self.total = 0
        self.picked: dict[str, int] = {}

    def picked_up(self, order: str, t: int) -> None:
        self.picked[order] = t

    def delivered(self, order: str, t: int) -> None:
        self.total += (t - self.picked[order]) * RATE   # 钱直接累加

class DerivedPay:
    def __init__(self) -> None:
        self.events: dict[str, dict[str, int]] = {}         # 只存事实：每单的时间点

    def record(self, order: str, kind: str, t: int) -> None:
        self.events.setdefault(order, {})[kind] = t      # 只存事实

    def total(self) -> int:
        return sum((e["delivered"] - e["picked"]) * RATE # 钱现算
                   for e in self.events.values() if len(e) == 2)

a = AccumulatedPay()
a.picked_up("o1", 0); a.delivered("o1", 20)
d = DerivedPay()

d.record("o1", "picked", 0); d.record("o1", "delivered", 20)
print("送达 20 分钟  累加:", a.total, "现算:", d.total())

# 送达时间被更正为 15 分钟
a.delivered("o1", 15)                                        # 只能再加一笔？减一笔？重复送达就多算
d.record("o1", "delivered", 15)
print("更正为 15 分钟 累加:", a.total, "现算:", d.total())
```

先送达 20 分钟，再更正为 15 分钟，实际输出：

```
送达 20 分钟  累加: 600 现算: 600
更正为 15 分钟 累加: 1050 现算: 450
```

**为什么。** 累加版本把更正当成又一次送达，多算了一笔（600+450）。要修它，得知道「上一次加了多少」：这就是在偷偷重建事实。

**代价。** 读要现算；事实少时无所谓，事实多时要靠随写入同步的派生索引（见第 4 张卡）。
