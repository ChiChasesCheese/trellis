---
id: hi-pt-multithreaded-logging-framework-2-api-and-poison
node: qb.lld.multithreaded-logging-framework.points
type: qa
step: 2
---
## Q
**多线程日志框架 · 核心类与毒丸**｜出自：多线程日志框架 › 核心实体与接口

日志框架对外接口是什么？内部有哪些队列，毒丸（poison pill）起什么作用？用到了哪些设计模式？

## A
**接口。** `log(level, message) -> Future` 与 `close()`；内部三个有界队列 `_incoming`、`_to_write`、`_to_ack` 和三个线程。
**毒丸。** 一个特殊对象沿流水线逐级传递，每一级收到后排空并退出。
**模式。** 生产者-消费者、有界阻塞队列做背压、观察者/回调（Future 承载确认）、策略（格式化器与 Appender）、门面。
