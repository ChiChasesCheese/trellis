---
id: hi-c-sd-dealing-with-contention-x05-reservation-lock
node: sd.patterns.dealing-with-contention.exam
type: qa
step: 5
---
## Q
**处理竞争 · 选座保留十分钟**｜考点 · 必会

订票系统要给选中座位保留十分钟。你会怎么选实现？只用 Redis `SET NX EX` 有什么风险？

## A
- **不用事务行锁：** 它占连接十分钟，堵住别人，且只在持有它的事务内可见。
- **选项：** 已有数据库就用 `reserved_by` / `reserved_until` 两列的条件写，过期自动视为空闲，无需新组件；追求速度用 Redis `SET NX EX`，过期自动清除；强一致要求高才上 ZooKeeper / etcd。
- **Redis 的风险：** 持有者停顿超过 TTL，锁被下一个人拿到，短暂两人同时认为自己持有；Redis 还是单点。座位软预留可容忍，会损坏数据的场景不行。
- **要点：** 保留之后，最终出票仍要对座位行做条件写，预留只是缩小争抢窗口和改善体验。
