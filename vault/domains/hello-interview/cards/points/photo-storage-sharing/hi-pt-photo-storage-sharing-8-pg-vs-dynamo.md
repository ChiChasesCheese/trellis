---
id: hi-pt-photo-storage-sharing-8-pg-vs-dynamo
node: qb.sd.photo-storage-sharing.points
type: qa
step: 7
---
## Q
**照片存储与分享系统 · 元数据库选 PostgreSQL 还是 DynamoDB**｜必会 · 出自：照片存储与分享系统 › 深入 3

照片元数据服务应选分片 PostgreSQL 还是 DynamoDB？各自在哪些访问模式上顺手或别扭？倾向哪个？

## A
**访问模式。** 几乎全部请求带 owner_id；按时间倒序分页；集合层级和多对多的小事务；跨用户分享读取；分析统计。
**PostgreSQL。** 二级索引、事务、递归查询现成；2 TB 按用户分 16 到 64 个分片，每片几十到一百多 GB；缺点是分片再平衡自己管。
**DynamoDB。** owner_id 分区键、`taken_at#photo_id` 排序键，时间线天然高效、零运维；集合移动、递归遍历、多对多事务别扭，分析无法直接做。
**判断。** 关系型加事务需求多、TB 级，倾向 PostgreSQL。
