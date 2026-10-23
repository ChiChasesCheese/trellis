---
id: hft-java-chronicle-vs-kafka-aeron
node: java.chronicle
type: qa
step: 4
---
## Q
Chronicle Queue、Aeron 和 Kafka 的定位有什么区别？该怎么选？

## A
- **Chronicle Queue**：同一台机器（或共享文件系统）上的进程之间，靠 mmap 文件共享，没有网络、没有 broker；延迟最低，可回放，但本身不跨机器（商业版提供复制）。
- **Aeron**：跨机器（UDP）或同机（IPC）的低延迟传输，本身不存储，加 Archive 才持久化。
- **Kafka**：分布式 broker 集群，有分区和副本，面向高吞吐和持久化，延迟通常是毫秒级，适合跨团队的数据管线。

选择：同机的日志或进程间通信选 Chronicle Queue 或 Aeron IPC；跨机器的热路径传输选 Aeron；要给很多下游团队分发数据、规模可扩展的研究或数据管线选 Kafka。
