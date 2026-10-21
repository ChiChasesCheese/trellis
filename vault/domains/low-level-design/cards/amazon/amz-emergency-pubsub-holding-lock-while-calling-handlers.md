---
id: amz-emergency-pubsub-holding-lock-while-calling-handlers
node: amazon.amz-emergency-pubsub
type: qa
step: 9
tags: [grown]
---
## Q
在应急发布订阅里，一个常见的错误是持有总线的锁去调用订阅者的处理函数，它会出什么问题？

## A
处理函数里很自然会再发布一条后续事件（火灾触发「疏散」事件）或退订自己。总线的锁不可重入，持锁调用时这次 `publish` 在同一线程上再拿锁，死锁。正确做法：持锁只拍订阅快照，释放后再逐个调用。例：A 收到 fire 后发布 evacuate，排在 A 之后的订阅者 R 先收到 evacuate、后收到 fire（嵌套的那次先送完），两条都能送到。
