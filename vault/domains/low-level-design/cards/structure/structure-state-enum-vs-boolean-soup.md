---
id: structure-state-enum-vs-boolean-soup
node: structure.state-machines
type: qa
step: 1
---
## Q
一个 `Order` 有 `is_paid`、`is_shipped`、`is_cancelled` 三个布尔字段。为什么这种写法会随需求增长而腐化，换成一个状态 `Enum` 具体换来什么？

## A
三个布尔值编出 2³ = 8 种组合，但只有大约 4 种是合法状态——没有任何东西阻止 `is_shipped=True` 同时 `is_cancelled=True` 这种非法组合出现，每个方法开头都要零散地拼凑一遍标志位判断。

换成单一的：

```python
from enum import Enum

class State(Enum):
    CREATED = "created"
    PAID = "paid"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"
```

之后：**非法状态变得不可表示**——一个字段、一个值；新增状态（如 REFUNDED）只需要加一个枚举成员加对应的转移规则，而不是再想一遍所有布尔组合该怎么处理。
