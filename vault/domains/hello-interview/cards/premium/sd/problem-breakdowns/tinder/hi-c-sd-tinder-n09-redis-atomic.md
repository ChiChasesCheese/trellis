---
id: hi-c-sd-tinder-n09-redis-atomic
node: sd.problem-breakdowns.tinder.notes
type: qa
step: 9
---
## Q
**Tinder · 深入一：Redis 原子判定**｜摘要 · 必会

为什么更推荐用 Redis 做实时匹配判定？Lua 脚本怎么保证原子，Redis 里的数据丢了怎么办？

## A
- **分工：** Cassandra 擅长耐久和海量存储，但不擅长实时匹配要的原子操作；Redis 在内存里做原子判定，Cassandra 继续当持久层。
- **数据结构：** 键是排序后的用户对，如 `swipes:123:456`，值是哈希（hash），两个字段各记一个人的滑动。同一对用户只有一个键，一个键只在一个节点上，所以原子性不跨节点。
- **原子性：** Redis 单线程执行命令，Lua 脚本整体不会被别的命令插入。脚本做两件事：先 HSET 写入自己的滑动，再 HGET 读对方的滑动；返回对方为 yes 且自己也是 yes，就创建匹配。
- **取舍：** 延迟低、可水平扩展；代价是要管理节点故障，以及扩缩容时哈希槽的迁移。
- **数据丢失：** Redis 只留最近的滑动，定期刷到 Cassandra，可以激进过期。节点丢失时最多漏掉近期滑动的匹配检测，历史仍在 Cassandra。
