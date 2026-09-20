---
id: structure-state-transition-table
node: structure.state-machines
type: qa
step: 2
---
## Q
"订单能不能从 PAID 直接变成 CANCELLED？"这类规则应该放在哪里？用 Python 写一个不暴露裸 setter 的状态转移检查。

## A
放进一张**声明式的转移表**，而不是散落在各处的 `if`：

```python
ALLOWED = {
    State.CREATED: {State.PAID, State.CANCELLED},
    State.PAID: {State.SHIPPED, State.CANCELLED},
    State.SHIPPED: {State.DELIVERED},
}

def transition_to(self, next_state: State) -> None:
    if next_state not in ALLOWED.get(self._state, set()):
        raise ValueError(f"{self._state} -> {next_state} not allowed")
    self._state = next_state
```

所有合法转移变成一张可以整体审阅的表；没有 `set_state()` 方法给调用方随意改状态，唯一入口是 `transition_to`，它自己查表校验。
