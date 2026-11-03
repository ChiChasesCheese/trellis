---
id: craft-dispatch-tables-3-transition-table
node: craft.idioms.dispatch-tables
type: qa
step: 3
---
## Q
**分派表 · 状态转移表为什么容易做穷举测试**｜写法

自动售货机有几个状态和几种事件，每个方法里都写 `if self.state != ...: raise` 很容易漏。把全部合法转移写成 `(状态, 事件) → 新状态` 的表，非法组合怎么处理，测试为什么能一次盖满？

## A
**要点。** 表里有的组合合法，没有的一律非法，规则只在一处写。因为键空间是有限的（状态数 × 事件数），可以用两层循环把所有组合都试一遍，数一数合法与非法各多少，不会漏掉「某个状态下某个事件」这种组合。表还能做结构检查，例如每个状态都能回到初始状态，不会卡死。

```python
from enum import Enum

class State(Enum):
    IDLE = "idle"; COIN = "coin"; DISPENSING = "dispensing"; CHANGE = "change"
class Event(Enum):
    PAY = "pay"; SELECT = "select"; DISPENSE = "dispense"; COLLECT = "collect"; REFUND = "refund"

TRANSITIONS = {
    (State.IDLE, Event.PAY): State.COIN,
    (State.COIN, Event.PAY): State.COIN,
    (State.COIN, Event.SELECT): State.DISPENSING,
    (State.COIN, Event.REFUND): State.IDLE,
    (State.DISPENSING, Event.DISPENSE): State.CHANGE,
    (State.CHANGE, Event.COLLECT): State.IDLE,
}

def fire(state: State, event: Event) -> State:
    try:
        return TRANSITIONS[(state, event)]            # 表里没有就是非法
    except KeyError:
        raise ValueError(f"{event.name} not allowed in {state.name}") from None

legal = illegal = 0
for s in State:                                       # 4 x 5 = 20 个组合各试一遍
    for e in Event:
        try:
            fire(s, e); legal += 1
        except ValueError:
            illegal += 1
print(legal, illegal)

reach = {State.IDLE}                                  # 每个状态都能回到 IDLE
while True:
    new = {s for (s, e), t in TRANSITIONS.items() if t in reach} - reach
    if not new: break
    reach |= new
print(reach == set(State))
```

实际输出：

```
6 14
True
```

**为什么。** 6 条合法、14 条非法，加起来是 20，说明没有遗漏。如果有人给枚举新增了一个状态，这段穷举代码自动把新组合算进非法，而不是静默通过。

**代价。** 表只描述「能不能转」，不描述转移时要做的动作（扣款、出货）。动作多且各不相同，就放在方法里，用表只守门；或者把值从状态改成 `(新状态, 动作函数)`。
