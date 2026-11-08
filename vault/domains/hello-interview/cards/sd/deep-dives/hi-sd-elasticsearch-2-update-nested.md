---
id: hi-sd-elasticsearch-2-update-nested
node: qb.sd.hotel-booking-system.pre-sd-deep-dives-elasticsearch
type: qa
step: 2
---
## Q
**更新的并发控制与 nested 取舍**｜系统设计 · 深入技术

同时有多个进程更新同一文档时，Elasticsearch 怎么避免互相覆盖？评论是嵌入书的文档（nested）还是单独成索引，怎么判断？

## A
**更新。** 整个文档覆盖写有风险：并发更新会丢对方的改动。写入响应里的 `_seq_no` 和 `_primary_term` 可用于乐观并发控制（optimistic concurrency control）：更新时带上 `if_seq_no` 和 `if_primary_term`，不匹配就报错，客户端处理冲突后重试（`_version` 只用于外部版本号）。`_update` 接口只改部分字段，不必先取回整个文档。

**为什么。** 集群是分布式、异步、并发的，请求可能分发到多个节点并乱序到达，更新语义要显式。

**nested 取舍。** 以「书和它的评论」为例：评论很少改、常和书一起查询，就嵌套进书文档，更高效；评论更新频繁，就单独建索引。这与 SQL 的规范化 / 反规范化权衡同类。
