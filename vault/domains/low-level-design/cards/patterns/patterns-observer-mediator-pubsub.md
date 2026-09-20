---
id: patterns-observer-mediator-pubsub
node: patterns.observer
type: qa
step: 5
---
## Q
Observer、Mediator 和 PubSub 都在"连接对象"，怎样区分它们，实际选型时又是怎么竞争的？

## A
- **Observer**：一个 subject 直接广播给多个观察者，观察者自己向 subject 注册。形状是一对多、直接调用。
- **Mediator**：多个对象通过一个中介互相协调，而不是彼此直接引用。形状是多对多、集中在一个类里。
- **PubSub**：发布者根本不知道有哪些订阅者，中间件（消息队列、事件总线）负责投递。形状是多对多、彻底解耦、通常异步。

选型上的竞争：简单的进程内通知优先用 Observer，实现最直接；对象之间的协调关系变复杂（表单里五个字段互相影响）时考虑 Mediator；需要跨进程、跨服务传递事件时才需要 PubSub。
