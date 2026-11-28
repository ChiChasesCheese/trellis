---
id: hi-c-lld-coordination-n08-actor-model
node: lld.concurrency.coordination.notes
type: qa
step: 8
---
## Q
**并发协调 · Actor 模型**｜摘要 · 必会

Actor 是什么？它为什么不需要锁？它在 Python 里怎么实现？

## A
- **三个特征：** 有邮箱（消息队列）；一次只处理一条消息；能给其他 actor 发消息
- **不需要锁：** 自己的状态只会被自己顺序访问；同步集中到邮箱这一个边界，业务逻辑里没有锁
- **实现：** 一个线程、一个 `queue.Queue` 作为邮箱，循环 `get` 后调用 `on_receive`；用带超时的 `get` 周期检查运行标志以便停机
- **由来：** 1970 年代提出，Erlang 把它做成语言和运行时；Akka、Orleans 是常见实现
