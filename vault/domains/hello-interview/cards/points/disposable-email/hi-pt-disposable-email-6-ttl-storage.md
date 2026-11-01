---
id: hi-pt-disposable-email-6-ttl-storage
node: qb.sd.disposable-email.points
type: qa
step: 6
---
## Q
**临时邮箱服务 · 到期数据的存储选型**｜出自：临时邮箱服务 › 深入 1

5 小时后邮件要便宜地消失。Redis、关系库定时删、Cassandra、DynamoDB 怎么比？选哪个？

## A
**对比。** Redis 全放内存，1 TB 常驻成本高；关系库大批 `DELETE` 有写放大和碎片；Cassandra 用写入 TTL + 时间窗口压缩（TWCS），整窗口过期后整个文件直接丢弃，几乎无删除成本；DynamoDB TTL 可用但删除可能延后。
**选择。** 宽列库，按 `address` 分区、`receivedAt` 排序；Redis 只放邮箱存在性和发布订阅。
