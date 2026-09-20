---
id: problems-splitwise-expense-immutable
node: problems.marketplaces.splitwise
type: qa
step: 6
tags: [grown]
---
## Q
分账（Splitwise）里一笔已经记录的开销，它的每人份额应该在什么时候算、怎么保存？这个选择让“撤销一笔开销”这个追问变成什么样的实现？

## A
在构造时算一次并冻结：`__post_init__` 里调用拆分策略算出份额，存成 `MappingProxyType` 只读视图，参与人存成 `tuple`，整个开销是 frozen dataclass。这样即使调用方事后修改了当初传给策略的那个字典，已经记好的账也纹丝不动——过去发生的事不该被现在的操作动摇；每次访问现算则会让历史随输入漂移。回报在追问处：撤销一笔开销不是去改那笔账，而是按份额取负记一笔反向账写回账本（会计里的红冲），流水因此保留完整历史，也不需要为“可撤销”给开销加任何可变字段。
