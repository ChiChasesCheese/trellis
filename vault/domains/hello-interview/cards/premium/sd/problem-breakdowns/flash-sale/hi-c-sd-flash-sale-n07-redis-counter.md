---
id: hi-c-sd-flash-sale-n07-redis-counter
node: sd.problem-breakdowns.flash-sale.notes
type: qa
step: 7
---
## Q
**限时抢购 · 深入一：把预留协调搬到 Redis**｜摘要 · 必会

用 Redis 计数器做预留怎么实现？比数据库快在哪，仍然有什么问题？

## A
- **做法：** 每个抢购一个计数器 `available:{productId}`（初值 1 万）；预留时检查大于零并减一。Redis 命令在主线程上串行执行，没有行锁和事务簿记，每次扣减都是内存里原子的一步，所以一个 key 上能比 Postgres 的一行多处理一个数量级的操作。
- **过期：** 再用一个有序集合 `expirations:{productId}`，成员是 reservationId、分数是 expiresAt；清理任务按分数找到到期的预留，删除并给计数器加回。预留本身也可存在 Redis，以 reservationId 为键。
- **原子性：** 减计数器和记录预留不能分开（减完崩溃就丢了一个单元），要用 **Lua 脚本**一次完成检查、扣减、记录。
- **问题一：** 状态分裂在两个系统。Redis 不再只是缓存，抢购期间它是真相来源的一部分，要考虑持久化、恢复和与数据库对账。
- **问题二：** 串行并没有消失，只是挪到更快的地方：所有预留仍然更新同一个计数器，单个 Redis 的上限在每秒几十万次简单操作，数千万人砸同一个 key，Redis 自己也会成为瓶颈。
