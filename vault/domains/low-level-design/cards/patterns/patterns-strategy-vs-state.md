---
id: patterns-strategy-vs-state
node: patterns.behavioral
type: qa
---
## Q
Strategy and state have the same UML — context delegates to a swappable interface. What are the two behavioral differences?

## A
- **Who switches, and when**: with **strategy**, the *client* picks one algorithm up front (pricing rule, sort order) and it rarely changes mid-flight; strategies don't know about each other. With **state**, the *states themselves* (or the context) drive transitions at runtime — `PaidState` decides the order moves to `ShippedState` — so states know their successors.
- **What the abstraction means**: strategies are **interchangeable ways to do the same thing** (any one is valid); states make the object **behave differently per lifecycle phase**, and most transitions between them are illegal.

Tell: requirements say "support multiple X algorithms" → strategy; "an order/elevator/game can be in phases with different allowed actions" → state.

## Q zh
Strategy vs State——都封装行为，区分点是什么？

## A zh
- **Strategy**：**客户端**选择算法，然后使用它。算法相互独立，不互相通信。例：排序策略、支付方法。生命周期：创建时选择，然后固定。
- **State**：对象**内部改变状态**并改变行为。状态相互转换。例：订单（pending → processing → shipped）。生命周期：对象内移动，通常基于发生的事情。

一句话：Strategy 是「客户选择算法」；State 是「对象改变其性质」。
