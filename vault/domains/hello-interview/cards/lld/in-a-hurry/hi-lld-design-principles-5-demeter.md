---
id: hi-lld-design-principles-5-demeter
node: lld.in-a-hurry.design-principles
type: qa
step: 5
---
## Q
**迪米特法则（Law of Demeter）**｜低层设计 · 速览

`order.getCustomer().getAddress().getZipCode()` 违反了什么原则？应该怎么改？链式调用都算违反吗？

## A
**要点。** 违反迪米特法则（最少知识原则）：方法只应与直接相关的对象交谈，不要穿透对象去够远处的部分。

**为什么。** 调用方此时知道了三个对象的内部结构，任何一个改了组织方式，调用方就坏。

**改法。** 在 Order 上提供 `getCustomerZipCode()`，由它内部完成导航；类的方法也尽量返回调用方需要的具体数据，或提供做完整件事的高层方法，而不是丢出复杂对象让人去挖。

**易错。** 方法链本身不是问题：`builder.setName("John").setAge(30).build()` 这类流式接口始终返回同一类型，没有泄露内部结构。问题只在于链式穿过多种不同对象。
