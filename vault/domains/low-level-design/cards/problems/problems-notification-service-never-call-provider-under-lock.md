---
id: problems-notification-service-never-call-provider-under-lock
node: problems.components.notification-service
type: qa
step: 10
tags: [grown]
---
## Q
通知服务的派发线程调用 `provider.send(envelope)` 时，能不能持有服务自己的锁？各个组件（限流器、去重表、队列）的锁该怎么安排？

## A
**绝不能持锁调用 provider**。渠道是外部代码：它可能很慢（网关三秒超时）、可能抛任何异常、甚至可能回调回来。持锁调用外部代码是死锁的标准配方——这和观察者模式里『不要在持锁状态下通知观察者』是同一条规则。服务的锁只在取 provider、改计数器、压延迟堆这几个瞬间持有。

锁按对象切开：限流器、去重表、模板库、分道队列各锁各的，服务再有一把。关键是它们之间**没有嵌套**——服务从不在持有自己的锁时去调另一个组件的加锁方法，于是根本不存在锁序（lock ordering）问题，也就不需要证明。

另一条配套纪律：`dead_letters` 和 `history` 这类属性返回**快照元组**，不是内部容器——调用方拿到手的东西不该能改写服务的状态；而且两者都有 `maxlen` 上限，死信不会把内存吃光。
