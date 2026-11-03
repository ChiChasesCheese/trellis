---
id: craft-event-time-vs-processing-time-1-replay-by-event-time
node: craft.architecture.event-time-vs-processing-time
type: qa
step: 1
---
## Q
**事件时间 vs 处理时间 · 迟到的额度包为什么不该让扣费失败**｜架构

额度系统有两类事件：发放额度包（grant）和扣费（charge）。事件 g1 在 t=1 发生，c1 在 t=5 扣 80，g2 在 t=2 发生，但网络延迟使它晚于 c1 才到达服务。如果服务按到达顺序逐条处理，会发生什么？应该怎样设计？

## A
**要点。** 区分事件时间（event time，事情真正发生的时刻）和处理时间（processing time，服务收到它的时刻）。业务结果应由事件时间决定：服务把事件当作事实存下来，每次需要结果时按事件时间排序重放。迟到的事件自然插到它该在的位置，后面的结果随之重算。

```python
@dataclass(frozen=True)
class Event:
    id: str
    kind: str          # "grant" 或 "charge"
    at: int            # 事件发生时间（event time）
    amount: int

def apply_in_arrival_order(arrivals: list[Event]) -> str:
    bal = 0
    for e in arrivals:
        if e.kind == "grant":
            bal += e.amount
        else:
            if bal < e.amount:
                return f"{e.id} 被拒：余额 {bal} < {e.amount}"   # 处理时间顺序下，额度包还没到
            bal -= e.amount
    return f"全部成功，余额 {bal}"

def replay(facts: list[Event]) -> str:
    # 按事件时间排序重放；同一时刻先额度包后扣费
    return apply_in_arrival_order(sorted(facts, key=lambda e: (e.at, e.kind == "charge", e.id)))

arrivals = [
    Event("g1", "grant", at=1, amount=50),
    Event("c1", "charge", at=5, amount=80),
    Event("g2", "grant", at=2, amount=50),      # 迟到：t=2 发生，但晚于 c1 才送到
]
print("按到达顺序:", apply_in_arrival_order(arrivals))
print("按事件时间重放:", replay(arrivals))
```

到达顺序为 `g1(t=1,+50)`、`c1(t=5,-80)`、`g2(t=2,+50)`，实际输出：

```
按到达顺序: c1 被拒：余额 50 < 80
按事件时间重放: 全部成功，余额 20
```

**为什么。** 按到达顺序处理，c1 在 g2 到达前就因余额不足被拒绝，而它在现实中本来够用；这是网络延迟把一个业务决定改了。排序键里的 `e.kind == "charge"` 是同一时刻的并列决胜：先额度包后扣费，让结果与到达无关。

**代价。** 每次重放要从头排序，事件多了开销大；实际可以保留快照加增量，或者只重放受迟到事件影响的那一段。
