---
id: hi-c-lld-design-principles-x06-demeter-judge
node: lld.in-a-hurry.design-principles.exam
type: qa
step: 6
---
## Q
**设计原则 · 哪些链式调用算违规**｜考点 · 必会

判断是否违反迪米特法则：(a) `order.customer.address.zip`；(b) `query.where(..).order_by(..).limit(10)`；(c) `list.stream().filter().map().toList()`。

## A
- **(a) 违规：** 一路穿过 `Order`、`Customer`、`Address` 三种对象
- **(b) 基本没问题：** 流式接口，每步返回同类型的查询对象
- **(c) 没问题：** 在同一条流水线上依次变换，不暴露内部结构
- **判断依据：** 链上对象类型是否变化并泄露内部组织
- **修法：** 给 `Order` 加一个返回邮编的方法
