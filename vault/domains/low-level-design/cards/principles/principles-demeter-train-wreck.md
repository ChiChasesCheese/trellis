---
id: principles-demeter-train-wreck
node: principles.coupling
type: qa
---
## Q
```java
order.getCustomer().getWallet().debit(total);
```
Name the smell, the fix, and one chained-call style that is NOT a violation.

## A
**Law of Demeter violation** (train wreck): the caller is coupled to the internal structure of `Order`, `Customer`, *and* `Wallet` — reshaping any of them breaks distant code.

Fix: tell, don't ask — `customer.charge(total)`; the traversal moves inside the owner.

Not a violation: fluent builders and streams — each link returns the builder itself or a fresh value, not a reached-into internal.

## Q zh
什么是 Demeter 法则的违反？为什么 train wreck 是个名字？

## A zh
Demeter 法则说你只应该和你的 "朋友" 交流——方法只应该调用：
- 它自己的类中的方法
- 参数对象的方法
- 本地创建或获取的对象的方法

Train wreck（火车碰撞）是因为每个点像一节火车车厢：`a.getB().getC().getD().doIt()`。每个点都是一个对象，链在一起像是无控制地滑动。这暴露了中间对象的内部结构。
