---
id: craft-transition-table-state-machine-3-three-encodings
node: craft.patterns.transition-table-state-machine
type: qa
step: 3
---
## Q
**转移表状态机 · 三种编码：什么时候选哪一种**｜模式

航班订单、自动售货机、外卖订单都用转移表，但表的形状各不相同：有的是 状态→允许的下一状态集合，有的是 (状态, 事件)→新状态，有的还带角色。它们各自适合什么问题？

## A
**要点。** 选择取决于「下一步由什么决定」：下一状态只看目标，用集合；转移由具体事件触发且同一状态下不同事件去不同地方，用 (状态, 事件)；同一个转移只有特定角色能做，用嵌套表。

```python
# airline：状态 → 允许的下一状态集合（调用方指明目标）
BookingStatus.HELD: frozenset({TICKETED, CANCELLED}),
BookingStatus.BOARDED: frozenset(),            # 终态：空集

# vending-machine：(状态, 事件) → 新状态（事件决定去向）
(State.COIN_INSERTED, Event.SELECT): State.DISPENSING,
(State.COIN_INSERTED, Event.REFUND): State.IDLE,

# food-delivery：状态 → {目标: 允许的角色}
OrderState.SCHEDULED: {
    OrderState.PLACED:    frozenset({Actor.PLATFORM}),
    OrderState.CANCELLED: frozenset({Actor.CUSTOMER, Actor.PLATFORM}),
},
```

以上各题的代码是节选：省略了类型标注、文档字符串和 `...` 处的细节，个别行为讲解而合并成一行，不是逐字摘抄。

不变：规则是数据，终态是空集（或没有出边），非法组合抛异常。变化：键的形状。叫车题里还把转移表和「谁可以取消」的许可表分成两张，因为两个问题的变化速度不同，合并后每加一种角色都要改转移表。

**见于。** airline、vending-machine、atm、ride-sharing、food-delivery、api-circuit-breaker、amz-robot-restaurant。

**信号。** 实体有生命周期，方法开头反复出现 `if self.status in (...)`；需求里出现「只有在……状态才能……」。
