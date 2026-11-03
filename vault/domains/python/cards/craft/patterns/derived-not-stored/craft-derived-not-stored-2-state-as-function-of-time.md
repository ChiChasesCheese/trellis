---
id: craft-derived-not-stored-2-state-as-function-of-time
node: craft.patterns.derived-not-stored
type: qa
step: 2
---
## Q
**派生而非存储 · 租车系统里「车现在停在哪」为什么没有 current_branch 字段**｜模式

租车预约可以提前很久创建。用户问的不只是「车现在在哪」，还有「下周三这辆车在哪」，用来判断下周三的预约能不能接。给车对象加一个 `current_branch` 字段，每次还车更新它，够用吗？

## A
**要点。** 不够。位置随时间变，而查询的时间点可以是未来。字段只能表示「现在」；未来的预约还没发生，没有任何地方能把它写进「当前位置」。把位置做成**时间的函数**：`location_at(moment)` = 最后一段在 `moment` 之前结束的行程的还车门店，没有就是基地门店。同一份行程表（事实），任何时刻的位置都能回答。

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Leg:
    start: datetime; end: datetime; origin: str; destination: str

class Car:
    def __init__(self, base): self.base, self.legs = base, []      # legs 按结束时间排好
    def add(self, leg): self.legs.append(leg); self.legs.sort(key=lambda l: l.end)
    def location_at(self, moment):
        """最后一段在此之前结束的行程的还车门店；没有就是基地门店。算出来的，不是存的。"""
        where = self.base
        for leg in self.legs:
            if leg.end <= moment: where = leg.destination
            else: break
        return where

d = lambda day, h=0: datetime(2026, 11, day, h)
car = Car("SFO")
car.add(Leg(d(2, 9), d(2, 18), "SFO", "LAX")); car.add(Leg(d(5, 9), d(5, 18), "LAX", "SEA"))
for day in (1, 3, 6): print(f"11/{day} 车在", car.location_at(d(day, 12)))
```

车从旧金山（SFO）出发，11/2 开到洛杉矶（LAX），11/5 开到西雅图（SEA）：

```
11/1 车在 SFO
11/3 车在 LAX
11/6 车在 SEA
```

**为什么。** 接受新预约时需要检查链的自洽：新预约的起点必须等于它前一段行程的终点（位置接续）。这个检查需要「它之前的位置」，是任意时刻的位置，不是当前位置。存字段版本在这里会逼你另写一套「预测位置」的逻辑，又是两份真相。

**代价。** 现算是 O(行程数)；行程表有序，可以用 `bisect` 在 O(log n) 里找到插入点，只检查前后邻居（见 `accepts`），代价不随表变大。

**信号。** 需求里出现「提前预约」「某个时刻的状态」「未来的可用性」，说明状态是时间的函数，不是一个字段。
