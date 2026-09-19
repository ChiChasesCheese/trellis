---
id: kafka-reliability-lag-timeouts-tuning
node: reliability.broker-config
type: qa
step: 6
source: kafka-2e
---
## Q
Kafka 2.5.0 把 `zookeeper.session.timeout.ms` 的默认值从 6 秒调大到 18 秒，把 `replica.lag.time.max.ms` 的默认值从 10 秒调大到 30 秒，动机是什么？把这两个超时调得更大，分别会带来什么正面和负面影响？

## A
动机是提高云环境下集群的稳定性：云上网络延迟波动更大，过短的超时容易把仅仅是短暂抖动（网络波动、垃圾回收停顿）的副本误判为「不同步」而移出 ISR，造成不必要的抖动。调大 `zookeeper.session.timeout.ms`（允许 broker 不发心跳的最长时间）能减少这种误判，但代价是真正宕机的 broker 要更久之后才会被判定为「死亡」并移出集群，故障检测变慢。调大 `replica.lag.time.max.ms`（允许副本落后多久仍算同步）同理能减少副本被误移出 ISR，但它也直接决定了消费者能等多久才能读到某条消息——值越大，消息「必须等所有同步副本复制完才可读」这一步骤可能拖得越久，消费延迟的上限也就越高（调大后最长可达 30 秒）。
