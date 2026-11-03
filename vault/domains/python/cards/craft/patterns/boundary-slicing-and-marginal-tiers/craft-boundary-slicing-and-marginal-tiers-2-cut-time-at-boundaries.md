---
id: craft-boundary-slicing-and-marginal-tiers-2-cut-time-at-boundaries
node: craft.patterns.boundary-slicing-and-marginal-tiers
type: qa
step: 2
---
## Q
**边界切分与边际阶梯 · 一段时间横跨高峰窗口边界，怎么计费**｜写法

配送员按时间计酬：每分钟 30 分，每天 18:00 到 19:00 是高峰，倍率 1.5。一单从 17:50 送到 18:20，跨过高峰开始的边界。「按开始时间判断整单倍率」会得到什么？该怎么计算才对？

## A
**要点。** 和金额阶梯同一个技巧：在所有边界处把区间切开，每一小段内部倍率恒定，各自计价再相加。切点 = 起止时间 + 严格落在区间内的所有边界（每天的窗口起止点）。因为每一小段内部不会再跨边界，判断它属于哪个窗口只要看**中点**。

```python
from datetime import datetime, time
from fractions import Fraction
from itertools import pairwise

RATE_PER_MIN = Fraction(30)                         # 每分钟 30 分
PEAK = (time(18, 0), time(19, 0), Fraction(3, 2))   # 18:00-19:00 倍率 1.5
covers = lambda t: PEAK[0] <= t < PEAK[1]           # 窗口也是半开的

def price_naive(start, end):
    mult = PEAK[2] if covers(start.time()) else 1    # 错：整段按开始时间的倍率
    return RATE_PER_MIN * mult * Fraction((end - start).total_seconds()) / 60

def price_sliced(start, end):
    cuts = {datetime.combine(start.date(), t) for t in (PEAK[0], PEAK[1])}
    points = sorted({start, end, *(c for c in cuts if start < c < end)})   # 在边界处切开
    total = Fraction(0)
    for a, b in pairwise(points):
        mid = a + (b - a) / 2                       # 每一小段内部倍率恒定：看中点就够
        mult = PEAK[2] if covers(mid.time()) else 1
        total += RATE_PER_MIN * mult * Fraction((b - a).total_seconds()) / 60
    return total

d = lambda h, m: datetime(2026, 11, 3, h, m)
for s, e in [(d(17, 50), d(18, 20)), (d(18, 10), d(18, 40)), (d(17, 0), d(17, 30)), (d(18, 40), d(19, 20))]:
    print(f"{s:%H:%M}-{e:%H:%M}  按开始时间: {float(price_naive(s, e)):7.1f}  切开: {float(price_sliced(s, e)):7.1f}")
```

四种情形（单位：分）：

```
17:50-18:20  按开始时间:   900.0  切开:  1200.0
18:10-18:40  按开始时间:  1350.0  切开:  1350.0
17:00-17:30  按开始时间:   900.0  切开:   900.0
18:40-19:20  按开始时间:  1800.0  切开:  1500.0
```

**为什么。** 按开始时间判断，会在跨边界的订单上同时出现少算（第一行）和多算（第四行），且只在跨边界时出错，不跨边界的两行完全一样，所以普通的例子测不出来。看中点而不是看起点：区间是左闭右开 `[a, b)`，起点恰好在边界上时中点仍能正确落进窗口内部，不用处理边界相等的特例。

**代价。** 切点数量随跨越的天数线性增长（每天每个窗口两个点），极长的区间（跨月）要先按天分组再算，或者用「整天的价格 × 天数 + 首尾两天零头」。

**易错。** 金额用精确分数（`Fraction`）累加，最后取整一次，见下一张卡。窗口跨午夜（22:00–06:00）时，窗口的结束点属于第二天，生成边界要把窗口结束时间算到 `day + 1`。
