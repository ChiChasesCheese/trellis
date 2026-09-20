---
id: quality-guard-clauses
node: quality.refactoring
type: qa
---
## Q
把嵌套条件换成 guard clause —— 展示这个变换，并说出"箭头形代码其实是另一个问题的症状"这条规则。

## A
```java
// 之前：happy path 被埋在三层里
if (user != null) { if (user.isActive()) { if (order.isPaid()) { ship(order); } } }

// 之后：尽早拒绝，happy path 平铺在最后
if (user == null)      return;            // 或者抛异常
if (!user.isActive())  throw new InactiveUserException(user.id());
if (!order.isPaid())   throw new UnpaidOrderException(order.id());
ship(order);
```

规则：guard 处理**异常**情况并立刻退出；主流程不带缩进、自上而下地读下来。多个 return 没问题 —— 单一出口那条规矩比垃圾回收还早。

症状自检：如果这些"guard"检查的是对象的*生命周期阶段*（`if (status == PLACED) ... else if (status == SHIPPED)`），真正的修法是 **state pattern**，而不是把条件写得更好看。
