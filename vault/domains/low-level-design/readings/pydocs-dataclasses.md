---
nodes: [python.dataclasses-enums]
url: https://docs.python.org/3/library/dataclasses.html
---
# dataclasses — Data Classes

值得读：`frozen`/`slots`/`order` 参数和 `field(default_factory=...)` 的官方语义，直接对应
`python-dataclass-frozen-post-init`、`python-dataclass-default-factory`、`python-dataclass-slots-cost` 三张卡——比如
可变默认值为什么必须用 `default_factory` 而不能写字面量，文档给的是权威解释，读它能补上这些参数组合背后真正在生成什么代码。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/dataclasses.html)

## Archived copy
![[src-python-docs-dataclasses-stack-overflow-clip]]
%% trellis:end %%
