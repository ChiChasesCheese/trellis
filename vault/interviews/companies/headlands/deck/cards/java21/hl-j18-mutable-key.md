---
id: hl-j18-mutable-key
node: java21.j18-comparators-interfaces
type: qa
step: 20
---
## Q
对象放进 `TreeSet` 后修改参与比较的字段会怎样？怎么避免？

## A
内部顺序就坏了，`contains` / `remove` 的行为不可预测（树的位置是按旧值放的）。

避免：用**不可变键**（如 `record`），或先从集合移除、改完再放回。
