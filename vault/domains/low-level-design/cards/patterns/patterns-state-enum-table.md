---
id: patterns-state-enum-table
node: patterns.state
type: qa
step: 2
---
## Q
用 `Enum` 加转移表实现状态机，在 Python 里长什么样？

## A
状态是 `Enum` 成员，转移规则是一个 `{(状态, 事件): 新状态}` 的字典；触发事件时查表，查不到就是非法转移，直接拒绝。

```python
from enum import Enum, auto

class VendingState(Enum):
    IDLE = auto()
    HAS_COIN = auto()
    DISPENSING = auto()

TRANSITIONS = {
    (VendingState.IDLE, "insert_coin"): VendingState.HAS_COIN,
    (VendingState.HAS_COIN, "select"): VendingState.DISPENSING,
    (VendingState.DISPENSING, "done"): VendingState.IDLE,
}
```
