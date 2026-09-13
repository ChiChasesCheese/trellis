---
id: kafka-admin-manual-topic-delete-requires-full-shutdown
node: admin.partition-reassignment
type: qa
source: kafka-2e
---
## Q
如果集群禁用了主题删除功能（`delete.topic.enable=false`），需要手动从 ZooKeeper 元数据里删掉一个主题时，为什么必须先关闭集群中**所有** broker，而不能在集群还在运行时直接改 ZooKeeper？

## A
broker 依赖 ZooKeeper 里保存的元数据来判断集群当前有哪些主题、分区分布在哪里；如果集群还在运行的时候直接从 ZooKeeper 删除主题相关节点，正在运行的 broker 手上缓存的元数据和 ZooKeeper 里的真实状态就会突然不一致，可能引发难以预料的集群不稳定甚至崩溃。因此手动删除的正确顺序是：先关闭集群里全部 broker，再删除 ZooKeeper 中 `/brokers/topics/` 下对应的节点以及各 broker 磁盘上该主题的分区目录，最后重启所有 broker 让它们以干净、一致的元数据重新加入集群。
