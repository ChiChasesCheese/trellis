---
id: problems-chat-messaging-hot-partition-time-bucketing
node: problems.social.chat-messaging
type: qa
step: 7
tags: [grown]
---
## Q
In a chat system whose message store partitions by conversation_id, what real production failure mode does one unusually large or active group/channel cause, and what fix does Discord's own engineering blog describe after migrating from Cassandra to ScyllaDB?

## A
One very active conversation (a large group or channel) can generate an order of magnitude more writes than a typical one, concentrating on a single partition and its owning storage node — Discord's engineering blog documents this hot-partition pattern causing latency spikes that, under quorum reads/writes, dragged down the whole cluster, on top of garbage-collection pauses severe enough to require manual node reboots. The documented mitigation is finer time-bucketing of the partition key (e.g. hourly rather than daily buckets) so a single busy conversation's writes are spread across more physical partitions, plus Discord's broader move to ScyllaDB, which cut their node count from 177 to 72 and improved p99 read latency from 40-125ms to 15ms.

## Q zh
在一个按 conversation_id 分区消息存储的聊天系统中，一个异常大或异常活跃的群/频道会导致什么真实的生产故障模式？Discord 官方工程博客在从 Cassandra 迁移到 ScyllaDB 之后描述了什么修复方法？

## A zh
一个非常活跃的会话（大群或频道）产生的写入量可能比普通会话高一个数量级，集中在单个分区及其所在的存储节点上——Discord 工程博客记录了这种热分区模式导致延迟飙升，并在 quorum 读写机制下拖慢了整个集群，同时还伴随着严重到需要人工重启节点的垃圾回收（GC）停顿。文中记录的缓解方法是把分区键的时间分桶做得更细（例如按小时而非按天分桶），把单个繁忙会话的写入摊到更多物理分区上；此外 Discord 更大范围地迁移到了 ScyllaDB，将节点数从 177 降到 72，并把 P99 读延迟从 40-125ms 降到 15ms。
