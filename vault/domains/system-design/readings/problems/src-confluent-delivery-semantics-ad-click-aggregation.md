---
nodes: [problems.search.ad-click-aggregation]
url: https://docs.confluent.io/kafka/design/delivery-semantics.html
tags: []
---
# Message Delivery Guarantees for Apache Kafka — Confluent Documentation

值得读：Kafka/Confluent 官方文档，说明幂等 producer（producer id + 序列号去重）与事务
（`read_committed` 隔离级别、offset 提交和输出写入的原子性）如何组合出端到端精确一次。
本题「深入探讨」第 4 节引用的机制描述来自这份文档，并把幂等 sink 的 upsert key 确定性
要求落到了本题的具体表结构上；这与既有卡片
[[async.delivery.exactly-once|Effectively Exactly-Once]] 的内容一致，文档本身还覆盖了
跨集群复制场景下事务边界不延伸的细节，本题在「常见错误」里只简要提及。
