---
nodes: [amazon.amz-robot-restaurant]
url: https://docs.python.org/3/library/enum.html
---
# enum — Support for enumerations（Python 标准库文档）

值得读：英文官方文档。订单状态、机器人状态、事件种类都适合写成 `Enum`；成员是单例，比较用 `is`。合法转移表可以是 `dict[RobotState, frozenset[RobotState]]`：枚举成员可以直接做字典的键。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/enum.html)

## Archived copy
![[src-python-docs-enum-linkedin-clip]]
%% trellis:end %%
