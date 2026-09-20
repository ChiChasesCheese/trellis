---
nodes: [problems.social.stack-overflow]
url: https://docs.python.org/3/library/dataclasses.html
---
# dataclasses — 事件与值对象为什么都是 `frozen=True, slots=True`

值得读：`VoteEvent`、`AcceptEvent`、`Comment`、`EditEntry` 在本题解里全部是
`frozen=True, slots=True` 的 `dataclass`。这一节说明了理由：一旦声望账本靠"事件不可变"
才能安全地被反复重放（`ReputationLedger.recompute`），任何一处允许原地修改事件字段的代码
都可能让增量缓存和重放结果对不上；`frozen=True` 把这条不变量交给解释器在赋值时报错，
而不是靠代码审查去保证。`slots=True` 则是这套系统里几十万条事件在内存里堆起来时，一个
不需要额外争论的从属优化。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/dataclasses.html)

## Archived copy
![[src-python-docs-dataclasses-stack-overflow-clip]]
%% trellis:end %%
