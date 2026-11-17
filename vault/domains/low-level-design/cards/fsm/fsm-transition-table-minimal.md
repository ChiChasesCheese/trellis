---
id: fsm-transition-table-minimal
node: fsm.transition-table
type: qa
step: 1
---
## Q
贷款有“待放款、已放款、已还清、已拒绝”几种状态。怎么用最小的代码实现状态转移？为什么用一张表，而不是 `if` 套 `if`？

## A
**转移 = 表里的一行：（状态，事件）→ 新状态**

- **表即规则**：想知道“已放款还能做什么”，读表的几行，不用读控制流；
- **加状态、加事件**：加行，不改查找的代码；
- **没有这一行就是非法**：查不到就明确拒绝，不会走进“什么也没发生”的分支；
- **状态用枚举**：拼写错误在导入时就暴露，而不是在运行时静默落空。

```python
from enum import Enum

class S(Enum):
    PENDING = "pending"; ACTIVE = "active"; REPAID = "repaid"; REJECTED = "rejected"

TABLE = {
    (S.PENDING, "disburse"): S.ACTIVE,
    (S.PENDING, "reject"): S.REJECTED,
    (S.ACTIVE, "settle"): S.REPAID,
}

def fire(state: S, event: str) -> S:
    try: return TABLE[(state, event)]
    except KeyError: raise ValueError(f"{event} not allowed in {state.value}") from None

print(fire(S.PENDING, "disburse"))              # S.ACTIVE
try: fire(S.ACTIVE, "disburse")
except ValueError as e: print(e)                # disburse not allowed in active
```

**知识点：**转移表（Transition Table）
