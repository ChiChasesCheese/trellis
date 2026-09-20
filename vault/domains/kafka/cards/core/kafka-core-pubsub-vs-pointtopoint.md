---
id: kafka-core-pubsub-vs-pointtopoint
node: core.pubsub-why
type: qa
step: 1
source: kafka-2e
---
## Q
一个数据发布者最初直接连接单个接收者传输监控指标；随着接收系统越来越多，点对点连接开始变得难以维护。发布与订阅系统（pub/sub messaging system）用什么方式解决了这个问题？

## A
pub/sub 系统在发布者和接收者之间加入一个独立的中间层，通常称为 broker（消息中转服务器）。发布者（publisher）不再直接把消息发给某个具体接收者，而是把消息发给 broker；订阅者（subscriber）按需向 broker 订阅特定类型的消息。这样发布者和订阅者互不感知对方的存在（解耦），新增一个消费系统只需向 broker 订阅即可，不必在原有系统上再拉一条新连接，避免了连接数随系统数量增长而爆炸式增加。
