---
id: hl-j02-final-redundant-immutable
node: java21.j02-sealed
type: qa
step: 21
---
## Q
`final record Ok(...)` 或 `final enum` 里的 `final` 有什么问题？`sealed` 和不可变性是什么关系？

## A
`final record` 不是错误，但**多余**：`record` 隐式 `final`，`enum` 同理。

`sealed` 管的是"**类型**有几种"，不管"对象的字段能不能改"。可变性靠 `record` / `final` 字段，两者互相独立：`sealed` 类型的实现照样可以有可变字段。
