---
id: craft-observability-as-design-2-record-the-change-when-it-happens
node: craft.architecture.observability-as-design
type: qa
step: 2
---
## Q
**可观测性即设计 · 网约车行程只存当前状态，客服问「这单几点被谁取消的」怎么办**｜架构

行程的状态机有 REQUESTED、MATCHED、CANCELLED 等状态，对象里只存当前状态就够业务运行了。可是客服每天都会问：这单几点取消的？司机取消还是乘客？原因是什么？能不能事后从当前状态推出来？

## A
**要点。** 不能。当前状态只回答「现在是什么」，不回答「怎么到这里的」。凡是会有人事后追问的状态变化，必须在**变化发生的那一刻**写下一条不可变的记录：何时、从哪到哪、谁、为什么。网约车题解里的 `StateChange` 就是这样，注释说「客服每天都要回答这单几点被谁取消的，这个问题只能靠事中记录，不能事后推算」。

```python
from dataclasses import dataclass
from enum import Enum

class State(Enum):
    REQUESTED = 1; MATCHED = 2; CANCELLED = 3

@dataclass(frozen=True, slots=True)
class StateChange:                         # 一次转移的留痕：何时、从哪到哪、谁、为什么
    at: int
    previous: State
    current: State
    by: str
    reason: str | None = None

class Trip:
    def __init__(self) -> None:
        self.state = State.REQUESTED
        self.history: list[StateChange] = []
    def transition_to(self, new: State, at: int, by: str, reason: str | None = None) -> None:
        self.history.append(StateChange(at, self.state, new, by, reason))   # 转移的同一刻写下
        self.state = new

t = Trip()
t.transition_to(State.MATCHED, at=100, by="system")
t.transition_to(State.CANCELLED, at=160, by="driver", reason="rider unreachable")
print("只有当前状态:", t.state.name)       # 客服问「几点被谁取消的」，这里答不出
last = t.history[-1]
print("事中留痕:", last.current.name, "at", last.at, "by", last.by, "-", last.reason)
```

实际输出：

```
只有当前状态: CANCELLED
事中留痕: CANCELLED at 160 by driver - rider unreachable
```

**为什么。** 把「改状态」收到唯一入口 `transition_to`，记录就不可能漏写：改状态和留痕是同一个动作。记录冻结，事后也没人能改写历史。

**代价。** 历史列表随行程增长；状态转移的次数有上限（状态机是有限的），通常很小，所以值得。高频事件则要换成采样或外部日志系统，原则不变：在发生的现场写，而不是事后重建。
