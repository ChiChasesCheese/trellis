---
id: kafka-internals-purgatory-delayed-response
node: internals.request-handling
type: qa
source: kafka-2e
---
## Q
Kafka 里的「炼狱（purgatory，一块临时保存未完成响应的内存区域）」是用来解决什么问题的？举一个会用到它的场景。

## A
有些请求不能立刻给出响应，因为响应依赖将来才会发生的事件——例如生产者设置 `acks=all`（要求所有同步副本确认才算写入成功）时，broker 收到消息并写入首领后还不能马上应答，必须等所有同步副本（in-sync replicas，ISR）复制完这条消息才能返回成功；再比如消费者的获取请求要求「有足够数据才返回」，也需要等待。这类还不能立即答复的请求会被放进炼狱里挂起，一旦满足条件（复制完成、数据凑够、或超时），broker 才把对应的响应从炼狱取出发给客户端，这样处理线程不需要为等待中的请求持续占用。
