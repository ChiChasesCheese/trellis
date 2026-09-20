---
nodes: [problems.social.task-management]
url: https://docs.python.org/3/library/enum.html
---
# enum — Support for enumerations

值得读：官方文档对 `Enum` 成员比较、穷尽性的说明，是本文 `ActivityType` 用 `Enum` 而不是
字符串常量表达一枚封闭事件种类集合的直接依据；也是"工作流状态该不该各建一个类"这条决策里
"状态只是一枚标签"这句判断的字面支撑——`Enum` 已经把"这是一个封闭、可比较、可穷尽的集合"
这件事表达清楚了，不需要再借助类层级去表达状态本身。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/enum.html)

## Archived copy
![[src-python-docs-enum-linkedin-clip]]
%% trellis:end %%
