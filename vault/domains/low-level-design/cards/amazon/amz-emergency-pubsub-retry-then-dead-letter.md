---
id: amz-emergency-pubsub-retry-then-dead-letter
node: amazon.amz-emergency-pubsub
type: qa
step: 7
tags: [grown]
---
## Q
在应急发布订阅里，三个订阅者 A、B、C 依次订阅火灾事件，B 的处理函数总是抛 `ZeroDivisionError`，B 设置 `max_attempts=2`。发布一条火灾事件后会发生什么？

## A
A、C 各收到一次且 `publish` 不抛异常；B 被调用两次都失败后，总线的死信列表里多一条 `DeadLetter(subscriber='B', reason=HANDLER_FAILED, attempts=2, error='ZeroDivisionError: …')`，B 的 `failed` 计数加 1。如果 B 第二次成功，就不产生死信，`delivered` 加 1。死信队列有上限（只留最近 N 条），内存有界。
