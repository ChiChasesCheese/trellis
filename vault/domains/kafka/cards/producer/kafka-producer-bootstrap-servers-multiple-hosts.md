---
id: kafka-producer-bootstrap-servers-multiple-hosts
node: producer.client-basics
type: qa
step: 2
source: kafka-2e
---
## Q
配置 `bootstrap.servers` 时，为什么建议至少填两个 broker 地址，而不是只填一个？

## A
`bootstrap.servers` 只是生产者用来建立到 Kafka 集群的初始连接的入口，一旦连上，生产者就能从这个 broker 那里获取到集群中其他 broker 的信息，并不需要在这里列出全部 broker。但如果只配置了一个地址而这台 broker 恰好停机，生产者就完全无法建立初始连接；配置至少两个地址，即使其中一个不可用，生产者仍能通过另一个连接到集群。
