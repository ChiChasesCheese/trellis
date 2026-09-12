---
id: kafka-admin-quota-throttle-per-broker
node: admin.dynamic-config
type: qa
source: kafka-2e
---
## Q
给某个生产者客户端配置了 10 MBps 的生产配额（quota，限制客户端能使用多少资源），在一个有 5 个 broker 的集群里，这个客户端实际能达到的总生产速率是多少？为什么答案取决于分区首领（leader）的分布？

## A
配额是按「客户端 - broker」这一对关系分别节流的，不是全局限制：客户端向每一个 broker 最多能以配置的速率（这里是 10 MBps）写入数据。如果这个客户端要写入的所有分区的首领均匀分布在 5 个 broker 上，它就能同时对每个 broker 都打满 10 MBps，总吞吐量可达 50 MBps；但如果这些分区的首领全部集中在同一个 broker 上，无论集群有多少台机器，这个客户端能达到的生产速率也只有 10 MBps。所以配额策略要发挥效果，前提是分区首领要在 broker 间均匀分布。
