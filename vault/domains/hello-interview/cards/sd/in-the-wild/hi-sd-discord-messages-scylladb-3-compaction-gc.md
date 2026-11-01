---
id: hi-sd-discord-messages-scylladb-3-compaction-gc
node: sd.in-the-wild.discord-messages-scylladb
type: qa
step: 3
---
## Q
**Discord 消息：压实积压与 JVM 停顿**｜系统设计 · 业界案例

Cassandra 集群为什么越来越难运维？压实积压为何会自我加剧，「gossip dance」是什么，JVM 垃圾回收带来什么问题？

## A
**压实积压的恶性循环。** Cassandra 靠压实控制 SSTable 数量，Discord 的集群经常追不上。未压实文件越积越多，读变慢；慢读消耗更多节点资源，压实可用的资源更少，积压继续增长。

**不能简单加大压实。** 压实和线上流量抢同一份 CPU 和磁盘，调高只会让延迟更差。

**gossip dance。** 工程师的补救办法：把一个节点摘出服务，让它不处理线上流量，专心压实；再放回来，等它重放期间错过的写入；然后对下一个节点重复。

**JVM 停顿。** Cassandra 运行在 JVM 上，垃圾回收器回收内存时会周期性暂停应用，表现为延迟尖刺，最坏的停顿长到运维人员必须重启节点并把它慢慢带回集群。

**后果。** 压实积压加 GC 停顿让集群脆弱，工程师花大量时间手工维持健康，这还没算热分区造成的问题。
