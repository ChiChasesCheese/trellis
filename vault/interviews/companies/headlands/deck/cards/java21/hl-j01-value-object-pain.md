---
id: hl-j01-value-object-pain
node: java21.j01-record
type: qa
step: 1
---
## Q
什么是值对象（value object）？Java 8 里写一个三字段的值对象要写多少样板代码，每加一个字段要同步改几处？

## A
值对象：一包只读数据（如成交 `(代码, 价格, 数量)`），创建后不再变，**内容相同就该视为同一个东西**。

Java 8 写三个字段约 **30 行**。每多一个字段要同步改 **7 处**：字段、构造器参数、赋值、getter、`equals`、`hashCode`、`toString`。漏改不报编译错，只会运行时悄悄出错。

Java 16 的 `record`（预览于 14、15）就是为消灭这些样板而生。
