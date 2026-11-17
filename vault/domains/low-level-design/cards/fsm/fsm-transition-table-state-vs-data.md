---
id: fsm-transition-table-state-vs-data
node: fsm.transition-table
type: qa
step: 3
---
## Q
还款“部分还款仍是已放款，还到 0 才是已还清”。是不是要给每种剩余金额各设一个状态？状态和数据怎么分？

## A
**状态是有限的类别，金额是数据**

- **状态**：个数固定、写得出来的类别：`active`、`repaid`；
- **数据**：未还金额这种连续取值，放在另一个字段里；
- **转移的结果取决于数据**：同一个“还款”事件，剩余为 0 时落在 `repaid`，否则仍是 `active`；这个选择放在转移函数的判断里（守卫），不放进表的键；
- **状态数炸掉**：键里放数据，状态个数和数据取值一样多，表不可维护。

```python
from dataclasses import dataclass

@dataclass
class Loan:
    state: str = "active"
    remaining: int = 100

def repay(loan: Loan, amount: int) -> None:
    if loan.state != "active" or not 0 < amount <= loan.remaining:
        raise ValueError("illegal")
    loan.remaining -= amount
    loan.state = "repaid" if loan.remaining == 0 else "active"

loan = Loan(); repay(loan, 30); print(loan)       # Loan(state='active', remaining=70)
repay(loan, 70); print(loan)                      # Loan(state='repaid', remaining=0)
```

**知识点：**转移表（Transition Table）
