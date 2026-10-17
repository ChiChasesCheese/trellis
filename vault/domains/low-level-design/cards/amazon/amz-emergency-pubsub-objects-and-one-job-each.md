---
id: amz-emergency-pubsub-objects-and-one-job-each
node: amazon.amz-emergency-pubsub
type: qa
step: 2
tags: [grown]
---
## Q
在应急发布订阅设计里，有哪几个核心对象？各自只负责哪一件事？

## A
`EmergencyBus`：注册表、给事件编号、路由、记死信，不知道处理函数做什么；`Subscription`：一个订阅者的过滤条件、重试次数和计数，一次 `deliver` 把失败吞在自己里面；`Mailbox`：只有异步订阅者才有，一条有界优先队列加一个工作线程；`EmergencyEvent`：冻结的事件快照；`DeadLetter`（死信）：一次没送到的记录，留着事后排查。划分依据：总线管「送给谁」，订阅者管「怎么接」，信箱管「什么时候接」。
