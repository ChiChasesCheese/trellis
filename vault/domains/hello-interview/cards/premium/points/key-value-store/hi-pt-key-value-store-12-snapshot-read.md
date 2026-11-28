---
id: hi-pt-key-value-store-12-snapshot-read
node: qb.sd.key-value-store.points
type: qa
step: 12
---
## Q
**分布式键值存储 · 过期与快照读**｜加分 · 出自：分布式键值存储 › 深入 8

分布式键值存储想支持带过期时间（TTL）和快照读。分别怎么做？

## A
**快照读。** 用每个键的版本号保留多个版本，按读时刻的版本取值。

**TTL。** 记录里带到期时间，读时判断过期，整理时顺带回收；二级索引也可以按同样的复制日志维护。
