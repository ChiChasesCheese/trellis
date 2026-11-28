---
id: hi-c-lld-coordination-n10-actor-challenges
node: lld.concurrency.coordination.notes
type: qa
step: 10
---
## Q
**并发协调 · Actor 的新问题**｜摘要 · 必会

Actor 去掉了锁，又带来了哪些新问题？

## A
- **邮箱溢出：** 和队列一样，生产者快于处理就满；要配置大小以及丢弃、阻塞或背压
- **消息顺序：** A 发给 B 的消息有序；A 和 C 同时发给 B 时交错顺序不确定，依赖全局顺序就复杂
- **调试：** 问题可能在消息流转，而不在某一段代码；追踪跨多个 actor 的请求比看调用栈难
- **请求-应答：** 异步，要自己建：消息里带回复地址再等响应；有的框架提供 ask 模式
