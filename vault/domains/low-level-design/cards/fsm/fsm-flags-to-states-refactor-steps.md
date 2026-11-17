---
id: fsm-flags-to-states-refactor-steps
node: fsm.flags-to-states
type: qa
step: 3
---
## Q
一个类已经有几个互斥布尔字段，外部代码到处在读它们。怎么安全地改成状态枚举？

## A
**先钉住行为，再换内部，保留旧接口**

- **第一步**：列出实际出现的取值组合，给每个合法组合起一个名字；
- **第二步**：为现有行为写测试，包括每个非法转移的拒绝；
- **第三步**：内部换成一个状态字段，原来的 `is_xxx` 保留为只读属性，调用方暂时不用改；
- **第四步**：把到处改标志的赋值，改成“转移函数”：检查当前状态、再改；
- **最后**：确认没有调用方再写那些旧字段，删掉属性。

```python
from enum import Enum

class St(Enum):
    PENDING = "pending"; ACTIVE = "active"; REPAID = "repaid"

class Loan:
    def __init__(self): self.state = St.PENDING
    @property
    def is_active(self): return self.state is St.ACTIVE      # 旧接口，只读
    def disburse(self):
        if self.state is not St.PENDING: raise ValueError(self.state.name)
        self.state = St.ACTIVE

loan = Loan(); loan.disburse(); print(loan.is_active)         # True
try: loan.disburse()
except ValueError as e: print("rejected:", e)                 # rejected: ACTIVE
```

**知识点：**把标志位改成状态（Flags to States）
