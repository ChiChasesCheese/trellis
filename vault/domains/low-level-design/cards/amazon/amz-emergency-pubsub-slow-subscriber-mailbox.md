---
id: amz-emergency-pubsub-slow-subscriber-mailbox
node: amazon.amz-emergency-pubsub
type: qa
step: 8
tags: [grown]
---
## Q
在应急发布订阅里，一个订阅者处理很慢（比如调用外部寻呼系统）会拖住发布者和其他订阅者，怎么办？信箱满了怎么处理？

## A
给慢订阅者配一个独立的信箱（有界优先队列加一个工作线程）：`publish` 只把事件放进信箱就返回，慢的只堵自己。信箱满了不阻塞发布者，而是挤掉「最不重要且最旧」的那条（可能就是新来的），记一条 `QUEUE_FULL` 死信。例：容量 2，信箱里是 i1、w1，来了 c1，则 i1 被挤掉；再来一条 i2，它比信箱里任何一条都不重要，被直接丢掉。
