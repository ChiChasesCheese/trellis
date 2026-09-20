---
id: problems-pub-sub-dead-letter-is-a-topic
node: problems.components.pub-sub
type: qa
step: 9
tags: [grown]
---
## Q
给进程内 Pub-Sub 加死信（dead letter）和通配订阅（`orders.*`、`orders.#`）时，怎么做才能不动投递路径？加通配之后必须补哪一条规则？

## A
死信主题**就是一个普通主题**：重试用尽的消息被原样发布到 `$dead-letter`，消息头里记下 `origin_topic`、`origin_seq`、`subscription`、`error`。要监控投递失败就 `subscribe("$dead-letter", ...)`，用的还是同一套 API，没有第二套机制；追加、读取、投递循环三个方法一行不动。

通配订阅的落点在『建主题』那一刻：新主题建出来时，遍历已注册的订阅，凡是模式匹配的就把位点挂上去——于是通配订阅对**以后才出现的主题**也有效，同样没碰投递路径。

必补的规则：**通配一律不匹配 `$` 开头的内部主题**。否则订了 `#` 的消费者会把自己投递失败产生的死信再吃一遍，失败一次就变成死循环。Kafka 用 `__consumer_offsets` 这样的内部主题名是同一个做法。
