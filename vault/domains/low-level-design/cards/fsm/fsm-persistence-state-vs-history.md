---
id: fsm-persistence-state-vs-history
node: fsm.persistence
type: qa
step: 1
---
## Q
贷款状态机要落盘，存当前状态，还是存事件历史？各自在什么情况下更合适？

## A
**当前状态好读，历史好审计**

- **存当前状态**：读最快，一行就是现在的样子；丢失的是“怎么走到这里的”，出了争议无法回放；
- **存事件历史**：当前状态是对事件的折叠（fold），任何时点的状态都能重算，天然可审计；代价是读要重放，通常配合定期快照；
- **两者可以并存**：状态表给读用，事件表给审计用，在同一个事务里同时写；
- **选择**：只关心现状、规则简单选前者；要对账、要解释历史、要修正过去的结果选后者；
- **事件不可改**：更正用一条新的冲正事件，不修改旧事件。

```python
def apply(loan, ev):
    kind, amt = ev
    if kind == "disburse": loan["state"], loan["remaining"] = "active", amt
    elif kind == "repay":
        loan["remaining"] -= amt
        loan["state"] = "repaid" if loan["remaining"] == 0 else "active"
    return loan

log = [("disburse", 100), ("repay", 30), ("repay", 70)]
state = {"state": "pending", "remaining": 0}
for ev in log: apply(state, ev)
print(state)                                         # {'state': 'repaid', 'remaining': 0}
print(apply({"state": "pending", "remaining": 0}, log[0]))    # 任意前缀都能重算
```

**知识点：**持久化与恢复（Persistence & Resume）
