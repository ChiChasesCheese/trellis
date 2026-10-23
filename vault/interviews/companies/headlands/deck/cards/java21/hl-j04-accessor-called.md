---
id: hl-j04-accessor-called
node: java21.j04-record-patterns
type: qa
step: 14
---
## Q
record 模式匹配时是直接读字段还是调用访问器？这对"重写访问器"和访问器的写法有什么影响？

## A
**真的调用访问器**（`invokevirtual Add.left()`），不是直接读字段。

影响：
- record 重写了访问器的话，模式匹配用的是**重写版**（这也是不建议重写访问器的原因）；
- 规范**不承诺访问器被调用的次数和顺序**，所以**让访问器无副作用**。
