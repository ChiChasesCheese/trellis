---
id: patterns-strategy-vs-state
node: patterns.behavioral
type: qa
---
## Q
Strategy vs State——都封装行为，区分点是什么？

## A
- **Strategy**：**客户端**选择算法，然后使用它。算法相互独立，不互相通信。例：排序策略、支付方法。生命周期：创建时选择，然后固定。
- **State**：对象**内部改变状态**并改变行为。状态相互转换。例：订单（pending → processing → shipped）。生命周期：对象内移动，通常基于发生的事情。

一句话：Strategy 是「客户选择算法」；State 是「对象改变其性质」。
