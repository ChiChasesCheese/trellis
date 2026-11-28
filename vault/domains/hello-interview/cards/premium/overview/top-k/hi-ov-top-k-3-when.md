---
id: hi-ov-top-k-3-when
node: sd.problem-breakdowns.top-k
type: qa
step: 3
tags: [通览]
---
## Q
**YouTube 热门 Top K · 深挖清单**｜通览

YouTube 热门 Top K 会被追问哪些深挖？各自的做法和代价是什么？

## A
- **少查库：** cron 预计算前 K 写缓存；请求不碰库；多一个 cron 要运维。
- **写入扩展：** 按视频 ID 分片，Flink 每分钟批量累加再写；每秒约 70 万次写；迟到事件要等水位线。
- **窗口查询：** 每个窗口一张聚合表加 views 索引；读回到 O(k)；一次写四张表。
- **滑动窗口：** 分钟粒度加增量减旧量，或只让小时窗口滑动；务实；要保留分钟明细。
- **近似：** Count-Min Sketch 加前 1000 名列表；省几百 GB；Redis 版宕机会丢状态，Flink 版可恢复。
- **专用数据库：** 时序库和实时 OLAP 预聚合；高基数靠预计算解决；InfluxDB 不适合，其余仍要缓存。

**各级别。** 中级端到端跑通；高级找出多数瓶颈并比较取舍；Staff 看清整个方案空间。
