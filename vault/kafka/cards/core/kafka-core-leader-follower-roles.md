---
id: kafka-core-leader-follower-roles
node: core.replication-isr
type: qa
source: kafka-2e
---
## Q
一个分区（partition）的多个副本（replica）分布在不同 broker 上时，为什么所有生产者的写请求都只能发给其中一个副本，而不能随便发给任意一个？

## A
每个分区的多个副本中只有一个是首领副本（leader replica），其余都是跟随者副本（follower replica）。为了保证一致性，所有生产者的写请求以及默认的消费者读请求都必须经过首领副本；跟随者副本的任务是不断从首领那里复制消息，让自己的状态与首领保持一致，而不直接处理客户端的写请求。如果首领所在的 broker 崩溃，会有一个跟随者被提拔为新首领。
