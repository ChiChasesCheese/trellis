---
id: hi-pt-top-k-counts-3-pipeline
node: qb.sd.top-k-counts.points
type: qa
step: 3
---
## Q
**Top-K 热门榜 · 预计算流水线**｜出自：Top-K 热门榜 › 整体设计

从事件到查询，Top-K 的整条链路怎么走？读路径碰数据库吗？

## A
**链路。** 事件进 Kafka（按对象 ID 分区）→ Flink 按分钟本地聚合（约 30 秒乱序水位线）→ 写按对象 ID 分片的存储（窗口桶 + 对象 → 计数）→ 每分钟归并各分片前 K → 写 Redis `topk:{窗口}:{对齐时间戳}`。
**读。** 查询服务只读 Redis，从不碰数据库；缓存保留几小时，预计算延迟时仍返回略旧的结果而不是报错。
