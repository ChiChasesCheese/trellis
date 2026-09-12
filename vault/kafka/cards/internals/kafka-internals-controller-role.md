---
id: kafka-internals-controller-role
node: internals.controller
type: qa
source: kafka-2e
---
## Q
在传统的基于 ZooKeeper（一个协调分布式系统元数据与选主的外部服务）的 Kafka 集群里，「控制器（controller）」和普通 broker（Kafka 服务器节点）是什么关系？它比普通 broker 多承担了什么职责？

## A
控制器本身也是集群里的一个普通 broker，同样接收生产者/消费者的读写请求；不同之处在于它额外承担了集群范围的元数据管理与**首领选举**：当某个分区的首领副本（leader replica）所在的 broker 下线时，由控制器决定这个分区的新首领是谁，并把这个决定告知集群里其它相关 broker。也就是说，一个集群只有一个控制器，但控制器不是脱离数据面的独立进程，它是被选出来「兼职」这份协调工作的那个 broker。
