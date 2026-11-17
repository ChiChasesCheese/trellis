---
id: debugging-prevent-three-layers
node: debugging.prevent
type: qa
step: 1
---
## Q
订单状态字符串里把 `"cancelled"` 拼成了 `"canceled"`，线上有一批订单没被取消。根因修好之后，还要做什么才能防止“同一类错误”再发生？测试、断言、类型各管哪一类？

## A
**修好根因只是一半：让这一类错误下次在更早、更便宜的地方暴露**

- **回归测试**：钉住这个具体的输入和期望，防止这一处被改回去；它只覆盖想到的用例；
- **断言 / 不变量检查**：在函数边界检查“状态必须是已知值”，错误值进来的当场就崩，不用等到下游出错；
- **类型 / 枚举**：让错误的值根本构造不出来；拼错 `Status.CANCELED` 是 `AttributeError`，在第一次执行那一行就暴露，比字符串拼错静默传播强得多；
- **越靠近源头越便宜**：类型（写代码时）早于断言（运行到那一行）早于测试（跑测试时）早于线上现象；
- **别指望单靠一种**：测试挡回退，类型挡拼写，断言挡数据层面的越界。

```python
from enum import Enum

class Status(Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"

class Order:
    def __init__(self): self.status = Status.ACTIVE

def cancel(order):
    order.status = Status.CANCELED          # 拼错：第一次执行就是 AttributeError
    return order

try: cancel(Order())
except AttributeError as e: print("立刻暴露：", e)
```

代码只演示类型这一层。字符串版本里 `order.status = "canceled"` 不会报错；错值一路传到读取处，才在某个 `if status == "cancelled"` 上悄悄走了错的分支。

**知识点：**防止复发（Prevent Recurrence）
