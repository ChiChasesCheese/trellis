---
id: hi-c-lld-design-principles-n06-demeter
node: lld.in-a-hurry.design-principles.notes
type: qa
step: 6
---
## Q
**设计原则 · 迪米特法则**｜摘要 · 必会

`order.getCustomer().getAddress().getZipCode()` 违反了什么？怎么改？所有链式调用都算违反吗？

## A
- **违反的是迪米特法则（最少知识原则）：** 一个方法只应和直接相关的对象交互，不应穿过一个对象去够它内部更远的对象。
- **问题在耦合：** 这行代码同时知道订单有客户、客户有地址、地址有邮编；其中任何一层改变组织方式，调用方就坏。
- **改法：** 在 `Order` 上提供 `getCustomerZipCode()`，由订单内部完成导航；调用方只拿到自己需要的数据，不必知道结构。设计类的方法时也是同理：返回具体数据或提供高层方法，而不是丢出一个复杂对象让别人去挖。
- **例外：** 同一类型的流式链（`builder.setName("John").setAge(30).build()`）每步返回同一个对象，没有泄露内部结构，不违反。
