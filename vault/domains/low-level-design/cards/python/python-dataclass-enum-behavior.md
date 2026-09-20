---
id: python-dataclass-enum-behavior
node: python.dataclasses-enums
type: qa
step: 6
tags: [grown]
---
## Q
Python 的 `Enum` 成员可以带方法吗？举一个订单状态的例子，说明这比一堆布尔值或裸字符串常量多提供了什么。

## A
可以——`Enum` 就是一个普通类，方法定义在类体里，`self` 就是当前成员；每个成员是**单例**，`==` 退化成 `is`（身份比较），天然防止拼写错误的字符串常量互相“意外相等”。
```python
from enum import Enum

class OrderState(Enum):
    CREATED = "created"
    PAID = "paid"
    SHIPPED = "shipped"

    def is_terminal(self) -> bool:
        return self is OrderState.SHIPPED
```
比起 `is_paid`/`is_shipped` 布尔值组合，`Enum` 把“当前只能处于一种状态”这个不变式直接编码进类型系统，状态相关的行为（如 `is_terminal`）也可以直接挂在枚举上，不用散落成一堆 `if`。
