---
id: kafka-internals-controller-leader-election-flow
node: internals.controller
type: qa
source: kafka-2e
---
## Q
控制器（controller）通过 ZooKeeper watch 或收到 `ControlledShutdownRequest`（有序关闭请求）发现某个 broker 离开了集群。它接下来要做哪几件事，才能让该 broker 上原来的分区首领恢复对外服务？

## A
控制器要依次做：1）找出这个下线 broker 上原本是**首领副本（leader replica）**的所有分区；2）为每个这样的分区从其副本集（replica set）里挑一个新首领（简单实现就是取副本列表中的下一个副本）；3）把这些新的首领/ISR（in-sync replicas，同步副本集合）状态以流水线（pipeline，异步批量发送以降低延迟）方式持久化回 ZooKeeper；4）向所有持有这些分区副本的 broker 批量发送 `LeaderAndISR` 请求，告知谁是新首领、谁是追随者；5）通过 `UpdateMetadata` 请求把变更广播给集群里全部 broker，更新它们本地缓存全部 broker/副本信息的 `MetadataCache`。收到 `LeaderAndISR` 的新首领即可开始处理生产者/消费者请求，追随者则开始从新首领拉取消息。
