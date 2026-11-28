---
id: bagu-link-ad-click-aggregator-1-map
node: links.ad-click-aggregator
type: qa
step: 1
---
## Q
**广告点击聚合 · 会被追问哪些八股**｜必会

设计广告点击聚合时，面试官最可能从哪几步下钻到基础知识？每一步问什么，怎么答？

## A
**基本回答。** 写多读少的流式聚合，点击不能丢也不能重复计。基础是：Kafka 的高吞吐与分区、去重幂等、内存预聚合与热点拆分、近似去重、对账。

**下钻路线。**
- 每秒百万点击为什么选 Kafka → 顺序写加批量压缩，按广告 ID 分区并行，[[b.mq.kafka-throughput|Kafka 为什么吞吐这么高]]
- 怎么不重复计数 → 事件带唯一 ID 去重，Kafka 恰好一次只管内部，[[b.mq.no-duplicate|重复消费与恰好一次]]
- 高峰积压、分区不够 → 转发到十倍分区的临时 topic，[[a.mq.backlog|消息积压怎么办]]
- 内存预聚合时热点广告成瓶颈 → 分片累加再合并，拆分热点 key，[[a.runtime.java-chm|ConcurrentHashMap 如何线程安全]]
- 按广告统计去重用户 → 展示用 HyperLogLog 近似，计费走精确路径，[[b.redis.bitmap-hll-geo|Bitmap、HyperLogLog、Geo]]
- 聚合结果为什么放列式 OLAP 而不是 MySQL → 按列扫描聚合快，明细冷热分离，[[b.search.nosql-selection|NoSQL 与 MongoDB 选型；Hive / Doris / 时序库了解级]]
- 点击突增是真是假 → 聚合前先过滤无效点击，[[a.protect.spike-10x|QPS 突增 10 倍怎么应对]]
- 流处理漏了怎么发现 → 原始事件落存储，批处理重算比对，[[a.idem.selection-reconciliation|分布式事务选型、最终一致与对账]]

**业务场景。** 抖音式按点击计费的广告，重复点击会多收广告主的钱，所以展示报表可以近似，计费必须走去重后的精确路径。
**系统设计。** [[links.metrics-aggregator|指标聚合系统（计数指标 + 直方图仪表盘）]]：同样先聚合后写入，但计数不要求去重；[[links.top-k-counts|Top-K 热门榜（视频播放、歌曲、话题标签）]]：同样的写入热点，输出的是榜单而不是按广告的计数。
