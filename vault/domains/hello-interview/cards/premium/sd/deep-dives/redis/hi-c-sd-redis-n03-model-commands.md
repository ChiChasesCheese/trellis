---
id: hi-c-sd-redis-n03-model-commands
node: sd.deep-dives.redis.notes
type: qa
step: 3
---
## Q
**Redis · 键与值、命令、哪些数据结构**｜摘要 · 必会

Redis 的数据模型和命令长什么样？键的设计为什么重要？

## A
- **键值模型：** 键是字符串，值是数据结构。例如键 `leaderboard:game:123` 的值可以是一个有序集合（玩家和分数）。
- **基础结构：** 字符串、哈希（对象 / 字典）、列表、集合、有序集合（可当优先队列）、流（追加式日志）、地理空间索引。Redis 8 把布隆过滤器、JSON、时间序列等概率与扩展结构也放进核心（旧版靠 Redis Stack 模块）。
- **2026 亮点：** 哈希可以给单个 field 设过期（Redis 7.4 的 `HEXPIRE` / `HTTL`，Redis 8 又加 `HGETEX` / `HSETEX`，Valkey 9.0 也支持）：一个 hash 存一个用户的多个子状态时，不必拆成很多带 TTL 的 key，也避免整个 hash 一起过期，读写时还能顺带续期。代价：需要 7.4+ / 9.0+，field 级过期要额外记录过期时间，内存和过期扫描成本要压测。
- **通信模式：** 发布订阅（Pub/Sub）和流，部分替代 Kafka、SNS / SQS 的角色。
- **命令：** 走简单的 RESP 协议，命令和参数的样子接近你在命令行敲的内容，如 `SET foo 1`、`INCR foo`、`XADD mystream * name Sara`。按数据结构分组很易读，如集合的 `SADD`（加元素）、`SCARD`（个数）、`SMEMBERS`（列出）、`SISMEMBER`（是否存在），对应任何语言里的集合操作。
- **键的设计就是数据的组织方式：** 键在集群里可能落在不同节点，所以你怎样组织键，就怎样扩展集群。
