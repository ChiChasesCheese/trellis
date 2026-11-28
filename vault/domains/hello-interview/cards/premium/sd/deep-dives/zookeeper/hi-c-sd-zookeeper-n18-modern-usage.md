---
id: hi-c-sd-zookeeper-n18-modern-usage
node: sd.deep-dives.zookeeper.notes
type: qa
step: 17
---
## Q
**ZooKeeper · 现在谁还在用 ZooKeeper**｜摘要 · 必会

ZooKeeper 现在还在哪些系统里？Kafka 的变化说明了什么趋势？

## A
- **仍然常见：** Apache 生态里很核心：HBase、Hadoop、SolrCloud、Storm、NiFi、Pulsar；ClickHouse 的复制协调、分布式 DDL 和元数据也依赖它。
- **Kafka 的转向：** Kafka 引入 KRaft（Kafka Raft 元数据模式），用自带的共识协议代替外部 ZooKeeper，目的是降低运维复杂度、去掉扩展瓶颈、减少故障点。
- **趋势：** 系统越来越倾向于内置共识，而不是依赖外部协调服务。
- **2026 亮点：** Kafka 4.0 起 ZooKeeper 模式已移除，被问“ZooKeeper 还用在哪”时不要再把新版 Kafka 列进去；Pulsar 5.0 的新集群也推荐用 Oxia 做元数据存储（ZooKeeper 仍支持）。
- **面试含义：** 设计新系统时不要默认引入 ZooKeeper，除非有明确理由。
