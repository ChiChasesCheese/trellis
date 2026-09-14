---
id: patterns-observer-mediator-pubsub
node: patterns.behavioral
type: qa
---
## Q
Observer vs mediator vs pub-sub — all decouple communicating objects. Separate them by topology and by who knows whom.

## A
- **Observer**: one-to-many, **subject knows its observers** (holds the list, calls them directly, usually synchronously). Observers know the subject to subscribe. Decouples subject from observer *types*, not existence.
- **Mediator**: many-to-many collapsed into a **star** — colleagues only know the mediator, which centralizes the interaction logic (air-traffic control, dialog coordinating its widgets). Use when peer-to-peer links have become a tangle; cost: the mediator can grow into a god object.
- **Pub-sub**: publisher and subscriber **don't know each other at all** — an event channel/broker sits between, often async. Strongest decoupling, weakest traceability.

Axis: how much the sender knows about receivers — observer (list of them) → mediator (one hub) → pub-sub (nothing).

## Q zh
Observer、Mediator 和 PubSub 都连接对象。怎样区分，何时竞争？

## A zh
- **Observer**：一个**主题**广播给多个**观察者**。观察者注册自己。形状：一对多、直接。
- **Mediator**：许多对象通过**中介**相互通信，而不是直接联系。形状：多对多、集中。
- **PubSub**：发布者不知道订阅者；中间件（消息队列、事件总线）承载。形状：多对多、解耦、通常异步。

何时竞争：简单的 UI 通知。Observer 最简单（直接注册）。Mediator 如果对象间通信变得复杂（对话框中的五个字段相互影响）。PubSub 如果你需要跨进程或微服务。
