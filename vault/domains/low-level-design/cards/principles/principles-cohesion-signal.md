---
id: principles-cohesion-signal
node: principles.coupling
type: qa
step: 1
---
## Q
单个类内部低内聚有什么表现？标准的重构方法是什么？

## A
信号：
- 字段聚成互不相交的几组，每组只被这个类的一部分方法用到；
- 类名要靠 "Manager"、"Util" 或 "Helper" 才能涵盖它做的所有事情；
- 方法之间既不互相调用，也不共享状态。

重构：沿着字段的使用聚类做**提取类（Extract Class）**，让拆出来的每个类的方法都用到自己大部分的字段。类内部的高内聚，是类与类之间能做到低耦合的前提。
