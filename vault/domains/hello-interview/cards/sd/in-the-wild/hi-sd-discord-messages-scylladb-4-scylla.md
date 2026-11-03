---
id: hi-sd-discord-messages-scylladb-4-scylla
node: sd.in-the-wild.discord-messages-scylladb.exam
type: qa
step: 4
---
## Q
**Discord 消息：换成 ScyllaDB 解决了什么、没解决什么**｜系统设计 · 业界案例

Discord 为什么把 Cassandra 换成 ScyllaDB？这一步能解决哪些问题，为什么仍然不够？

## A
**做法。** ScyllaDB 与 Cassandra 使用相同的查询语言和数据模型，但用 C++ 实现，不跑在 JVM 上。Discord 可以保留原有表结构，同时消除造成许多延迟尖刺和稳定性事故的垃圾回收器。

**其他好处。** 采用每核一片（shard-per-core）架构，每个 CPU 核心处理节点数据和请求的各自分片，单机性能更好，修复（repair）更快，运维工作量下降。

**解决了。** 存储层更快、更易运维。

**没解决。** 换数据库不会消除热分区：ScyllaDB 能让每次读更便宜，却无法阻止成千上万人请求同一分区里的消息。

**要点。** 「更快的数据库」和「更少的数据库工作」是两个不同的问题。要解决第二个，必须在数据库之前减少到达它的读请求数量。
