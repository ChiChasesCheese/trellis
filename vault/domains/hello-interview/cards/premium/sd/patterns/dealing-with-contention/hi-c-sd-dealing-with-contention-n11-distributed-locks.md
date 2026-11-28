---
id: hi-c-sd-dealing-with-contention-n11-distributed-locks
node: sd.patterns.dealing-with-contention.notes
type: qa
step: 11
---
## Q
**处理竞争 · 分布式锁**｜摘要 · 必会

用户选中座位后要保留十分钟让他填支付信息，为什么 `FOR UPDATE` 做不到？分布式锁有哪几种实现？

## A
- **为什么不行：** 行锁只活在一个事务里，会占着连接十分钟，还堵住所有要这行的事务，且别的无状态服务器看不到它。改成把锁当数据存：记录谁持有、何时到期，任何服务器都能读，不依赖某个事务。
- **Redis + TTL：** `SET key value NX EX` 原子创建并自动过期，`NX` 防止覆盖别人的锁。快而简单。缺点：持有者停顿超过 TTL（长 GC、网络慢）时锁被别人拿走，短暂两人同时认为自己持有；Redis 本身是单点。座位软预留可以接受，会损坏数据的场景不能只靠它。
- **数据库两列：** `reserved_by`、`reserved_until`，条件写 `WHERE reserved_until IS NULL OR reserved_until < NOW()`，过期自动视为空闲，无需清理任务；无新组件，但更慢，锁行本身可能成为热点。
- **ZooKeeper / etcd：** 基于共识（ZAB / Raft），分区下仍保持一致；ZooKeeper 的临时节点（ephemeral node）在客户端会话结束时自动消失。代价是运维一套协调集群。
- **额外收益：** 把争抢窗口缩到"选座瞬间"，没人填完支付才被告知座位没了。
