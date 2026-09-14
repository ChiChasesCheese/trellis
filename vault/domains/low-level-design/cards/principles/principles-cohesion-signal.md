---
id: principles-cohesion-signal
node: principles.coupling
type: qa
---
## Q
What does low cohesion look like *inside* a single class, and what's the standard refactor?

## A
Signals:
- fields cluster into disjoint groups, each used by a different subset of methods
- the name needs "Manager", "Util", or "Helper" to cover everything
- methods neither call each other nor share state

Refactor: **Extract Class** along the field-usage clusters, so each class's methods use most of its fields. High cohesion inside classes is what makes low coupling between them possible.

## Q zh
单个类内部低内聚的表现是什么，标准的重构方法是什么？

## A zh
信号：
- 字段聚集成不相交的组，每组被不同的方法子集使用
- 名字需要加上 "Manager"、"Util" 或 "Helper" 来涵盖所有东西
- 方法之间既不相互调用，也不共享状态

重构：沿着字段使用的聚类进行 **提取类（Extract Class）**，让每个类的方法使用大部分的字段。类内部的高内聚是使类之间的低耦合成为可能的前提。
