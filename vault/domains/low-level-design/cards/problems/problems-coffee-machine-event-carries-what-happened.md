---
id: problems-coffee-machine-event-carries-what-happened
node: problems.machines.coffee-machine
type: qa
step: 8
tags: [grown]
---
## Q
咖啡机的缺料告警事件里应该放什么？只写一句『牛奶低了』让订阅者自己去查库存，问题在哪？

## A
事件要自带订阅者需要的全部字段：哪种原料、**还剩多少**、警戒线是多少，做成一个 frozen dataclass。只写名字的话，订阅者必须回头调用库存的查询方法，而那是一次**没有持锁保护的、事后的**读取——中间可能又做掉了两杯，读到的数字和触发告警的那一刻已经不是一回事。通用原则是：**事件携带发生了什么，订阅者就永远不需要反向查询主体**。附带好处是事件天然可序列化，把它发往消息队列做集中监控时不需要回头查任何东西。
