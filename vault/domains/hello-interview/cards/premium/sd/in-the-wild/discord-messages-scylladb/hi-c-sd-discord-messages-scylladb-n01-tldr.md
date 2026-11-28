---
id: hi-c-sd-discord-messages-scylladb-n01-tldr
node: sd.in-the-wild.discord-messages-scylladb.notes
type: qa
step: 1
---
## Q
**Discord 消息存储 · 全貌**｜摘要 · 必会

Discord 的消息存储遇到了哪几类问题？最后用什么办法，结果如何？

## A
- **起点：** 2022 年初，177 个 Cassandra 节点存着万亿级消息。Cassandra 适合写多的负载，真正的麻烦在读。
- **三类问题：** 热门频道让成千上万个读请求砸向同一个分区，拖慢同机器上无关的查询；压实（compaction）积压；JVM 垃圾回收（GC）停顿让集群难运维。
- **两步方案：** 用 ScyllaDB（C++ 重写的 Cassandra 兼容数据库）换掉 Cassandra，解决库内的问题；在数据库前面放 Rust 数据服务，把同一频道的请求路由到同一实例，并合并重叠的相同读，减少到达数据库的读。
- **结果：** 177 个节点变 72 个；p99 读延迟从 40~125 ms 的区间变成稳定的 15 ms。
- **核心洞察：** 让每次读更便宜，和让读的次数更少，是两个不同的问题。
