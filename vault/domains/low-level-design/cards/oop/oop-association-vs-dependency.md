---
id: oop-association-vs-dependency
node: oop.relationships
type: qa
step: 1
---
## Q
一种设计里 `NotificationService` 是 `OrderService` 构造注入的字段，另一种里它是 `checkout(cart, notifier)` 的参数。分别说出这两种关系是什么，以及这个选择传达了什么信号。

## A
- **字段** → association（关联）：结构性的、长期存在的——"`OrderService` *拥有* 一个 notifier"。
- **参数/局部变量** → dependency（依赖）：一次性的 uses-a，是最弱的耦合。

信号：只要还只有一个操作需要它，就让它停留在 dependency；等到大多数方法都要用，再升级成 association。**能用的最弱关系胜出**——它把一次改动可能波及的范围压到最小。
