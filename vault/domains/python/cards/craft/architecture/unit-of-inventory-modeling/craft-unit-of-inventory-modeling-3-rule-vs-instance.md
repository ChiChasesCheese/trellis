---
id: craft-unit-of-inventory-modeling-3-rule-vs-instance
node: craft.architecture.unit-of-inventory-modeling
type: qa
step: 3
---
## Q
**库存的单位怎么选 · 「MU5100 每天 8 点起飞」能直接拿来卖票吗**｜架构

排班表上有一行规则：航班 MU5100，每天 08:00 起飞，机型 A320，180 座。订座系统要卖票。库存（已售张数）该挂在这条规则上吗？取消 7 月 1 日这一班时会发生什么？

## A
**要点。** 规则没有日期，不是可以被卖掉的东西。可卖的单位是航班实例（FlightInstance）：规则钉到某一天，库存、座位图和锁都长在实例上。选错单位的症状是需要大量特判才能表达「同一条规则的不同日期」；选对之后，取消某一天只动那一个实例，规则和其他日期都不受影响。

```python
from datetime import date, time, timedelta

@dataclass(frozen=True)
class Flight:                              # 排班规则：没有日期，不能卖
    number: str
    departs_at: time
    seats: int

class FlightInstance:                      # 某一天的那一班：可卖的单位，库存长在这里
    def __init__(self, flight: Flight, day: date) -> None:
        self.flight, self.day, self.sold, self.cancelled = flight, day, 0, False
    def book(self) -> bool:
        if self.cancelled or self.sold >= self.flight.seats:
            return False
        self.sold += 1
        return True

class Schedule:
    def __init__(self) -> None:
        self._instances: dict[tuple[str, date], FlightInstance] = {}
    def instance(self, flight: Flight, day: date) -> FlightInstance:    # 用到时才建
        return self._instances.setdefault((flight.number, day), FlightInstance(flight, day))

mu = Flight("MU5100", time(8, 0), seats=1)
sched = Schedule()
d1, d2 = date(2026, 7, 1), date(2026, 7, 2)
print("7/1 订:", sched.instance(mu, d1).book(), "| 7/1 再订:", sched.instance(mu, d1).book())
print("7/2 订（同一规则，库存独立）:", sched.instance(mu, d2).book())
sched.instance(mu, d1).cancelled = True            # 取消 7 月 1 日这一班
print("取消 7/1 后，7/3 不受影响:", sched.instance(mu, d2 + timedelta(days=1)).book())
```

座位 1 个；7/1 订两次，7/2 订一次，取消 7/1 后订 7/3，实际输出：

```
7/1 订: True | 7/1 再订: False
7/2 订（同一规则，库存独立）: True
取消 7/1 后，7/3 不受影响: True
```

**为什么。** 电影订座同理：座位的物理属性（排号、舱位）是不变的，所有场次共用，按场次独立的是「这一场的占用状态」。把占用写在座位上，一个场次的订座就会泄漏到所有场次。

**代价。** 实例要按需创建并有清理策略（飞完的航班实例不能永远留着）；大量实例的创建可以懒加载，如上面的 `setdefault`，也可以提前批量生成，取决于查询是否需要列出尚未有人订的班次。
