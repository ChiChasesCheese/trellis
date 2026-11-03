---
id: craft-thin-service-fat-domain-3-three-layers
node: craft.architecture.thin-service-fat-domain
type: qa
step: 3
---
## Q
**服务层薄、领域对象厚 · 停车费为什么拆成价目表、计费引擎、收费台三层**｜架构

停车场收费要算：每小时多少钱、每天封顶多少，还要处理入场开票、出场结算。把这些全写进一个 `ParkingLot` 类，测「2.5 小时收多少钱」要先造停车场、开票、手动改时间。怎么拆才能让每一层单独可测？

## A
**要点。** 三层各自只负责一种事：价目表（Tariff）是纯数据，计费引擎（FeeEngine）是纯计算，不知道票存在哪；收费台（FeeDesk）才是有状态的入口，开着的票只存一份，出场时在锁内取走，同一张票不可能被结算两次。计算规则的变化只动引擎，状态的变化只动收费台。

```python
@dataclass(frozen=True)
class Tariff:                          # 层一：纯数据（价目表）
    per_hour: Decimal
    daily_cap: Decimal

@dataclass(frozen=True)
class Ticket:
    id: str
    entered_at: datetime

class FeeEngine:                       # 纯计算，不知道票存在哪
    def __init__(self, tariff: Tariff) -> None:
        self.tariff = tariff
    def fee(self, ticket: Ticket, exited_at: datetime) -> Decimal:
        hours = -(-(exited_at - ticket.entered_at) // timedelta(hours=1))   # 向上取整
        return min(self.tariff.per_hour * hours, self.tariff.daily_cap)

class FeeDesk:                         # 有状态入口，开着的票只存一份
    def __init__(self, engine: FeeEngine) -> None:
        self._engine, self._open = engine, {}
    def enter(self, plate: str, at: datetime) -> Ticket:
        self._open[plate] = t = Ticket(f"T{len(self._open) + 1}", at)
        return t
    def exit(self, plate: str, at: datetime) -> Decimal:
        return self._engine.fee(self._open.pop(plate), at)      # 取走：同一张票不会结两次

t0 = datetime(2026, 1, 1, 9, 0)
engine = FeeEngine(Tariff(Decimal("5"), Decimal("30")))
# 测引擎：不需要 Desk，不需要状态
print("引擎 2.5 小时:", engine.fee(Ticket("x", t0), t0 + timedelta(hours=2, minutes=30)))
print("引擎 10 小时封顶:", engine.fee(Ticket("x", t0), t0 + timedelta(hours=10)))
desk = FeeDesk(engine)
desk.enter("沪A1", t0)
print("入口出口:", desk.exit("沪A1", t0 + timedelta(hours=1)))
try:
    desk.exit("沪A1", t0 + timedelta(hours=2))
except KeyError:
    print("同一张票不会结两次")
```

每小时 5、封顶 30；引擎算 2.5 小时和 10 小时，收费台走一遍入场出场，再出场一次，实际输出：

```
引擎 2.5 小时: 15
引擎 10 小时封顶: 30
入口出口: 5
同一张票不会结两次
```

**为什么。** 引擎的测试只要造一张票和一个出场时间，覆盖所有计费边界（不足一小时、跨天、封顶）；收费台的测试只关心状态：重复入场、重复出场、查找。两边不用互相造对方的环境。

**代价。** 层数多了，简单需求也要走三个类；只有在计算规则复杂、状态规则也复杂时，这样拆才划算。
