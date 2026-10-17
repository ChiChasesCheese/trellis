---
nodes: [amazon.amz-robot-restaurant]
url: https://docs.python.org/3/library/enum.html
---
# enum — Support for enumerations（Python 标准库文档）

值得读：英文官方文档。本题解的订单状态、机器人状态、事件种类都是 `Enum`；成员是单例，比较用 `is`。合法转移表则是一个 `dict[RobotState, frozenset[RobotState]]`，文档没有讲，但它说明了为什么枚举成员可以直接做字典的键。
