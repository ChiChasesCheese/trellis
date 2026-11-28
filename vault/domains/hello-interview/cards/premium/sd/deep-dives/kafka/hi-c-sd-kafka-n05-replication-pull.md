---
id: hi-c-sd-kafka-n05-replication-pull
node: sd.deep-dives.kafka.notes
type: qa
step: 5
---
## Q
**Kafka · 副本机制和拉取模式**｜摘要 · 必会

分区的副本怎么分工？leader 挂了怎么办？为什么消费者是主动拉取？

## A
- **leader-follower：** 每个分区有一个 leader 副本，处理所有写请求，默认也处理读请求（2.4 起支持从 follower 读，用来降延迟）；leader 的分布由集群控制器管理，使负载均匀分散。
- **follower：** 在其他 broker 上，不直接服务客户端，被动复制 leader 的数据，充当备份，并持续与 leader 同步。
- **故障转移：** 控制器监控所有 broker 的健康，一个 broker 挂了，就把 leader 角色交给一个同步的 follower，尽量减少停机和数据丢失。
- **拉取（pull）模式：** 消费者按自己的节奏主动轮询 broker。这是有意的设计：消费者自己控制速率，简化故障处理，不会压垮慢的消费者，也方便批处理。
- **2026 亮点：** 云上三副本跨可用区复制的流量费（AWS 约 0.02 美元/GiB）是 Kafka 最大的基础设施成本之一；消费端开 Fetch From Follower 加机架感知，读同可用区的副本。对延迟不敏感的日志、埋点还可以用把数据直接写进对象存储的方案（WarpStream、Confluent Freight；社区的 Diskless Topics KIP-1150 已接受但未发布），用延迟换成本（Freight 官方给的延迟最高一两秒）；支付链路仍用传统副本复制。
