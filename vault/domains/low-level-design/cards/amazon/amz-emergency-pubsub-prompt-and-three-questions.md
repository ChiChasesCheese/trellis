---
id: amz-emergency-pubsub-prompt-and-three-questions
node: amazon.amz-emergency-pubsub
type: qa
step: 1
tags: [grown]
---
## Q
Amazon 面试里「应急事件发布订阅（Emergency Pub/Sub）」怎么问的？开场先问哪三个澄清问题？

## A
报告的原话：有一个应急响应系统，一些组件订阅（subscribe）应急事件，另一些组件发布（publish）事件，请实现处理发布和订阅逻辑的类。先问三件事：(1) 事件在发布线程里同步送，还是异步送？决定要不要给订阅者配队列和线程；(2) 订阅者处理时抛异常怎么办？是重试、记录还是直接忽略；(3) 订阅者能按事件类型或严重度过滤吗，紧急事件要不要优先送？
