---
id: hi-c-lld-patterns-n09-observer
node: lld.in-a-hurry.patterns.notes
type: qa
step: 9
---
## Q
**设计模式 · Observer：事件订阅与通知**｜摘要 · 必会

Observer 在什么需求里出现？结构是什么？

## A
- **触发词：** 需求里出现"通知"或"更新多个组件"，例如股价变化后多个显示器要更新，或用户下单后库存、通知、分析系统都要知道。
- **结构：** 被观察者（`Subject`）提供 `attach`、`detach`、`notify`，观察者（`Observer`）提供 `update`；价格改变时，被观察者遍历所有已订阅的观察者并调用 `update`。
- **为什么好：** 被观察者不需要知道观察者拿数据做什么，也不需要知道有多少个，新增一个订阅者不用改被观察者，两边解耦。
- **地位：** 在面试里属于第一梯队模式。
