---
id: hi-c-sd-redis-n07-cache
node: sd.deep-dives.redis.notes
type: qa
step: 7
---
## Q
**Redis · 作为缓存：TTL、淘汰与热点键**｜摘要 · 必会

用 Redis 做缓存时 TTL 和淘汰各解决什么？它自己解决不了什么？

## A
- **映射直接：** 缓存键就是 Redis 键，缓存值就是 Redis 值，例如 `product:123` 存 JSON 或含名称、价格、库存的哈希。容量不够就加节点。
- **TTL 管陈旧度：** Redis 保证过期后不会读到那个键的值。
- **2026 亮点：** 过期粒度可以细到哈希的单个 field（`HEXPIRE`，Redis 7.4+ / Valkey 9.0+）：一个 hash 存一个用户的多个子项（会话、多租户缓存）时，不必拆成很多带 TTL 的 key。
- **TTL 不管内存压力：** 开箱即用时，内存满了 Redis 会拒绝写入。做缓存要配淘汰策略，如 `allkeys-lru`，丢掉最近最少使用的键腾空间。Redis 用抽样近似 LRU，而不是维护精确顺序，对缓存足够。
- **解决不了的：** 热点键（hot key）——单个键吸走不成比例的流量。这不是 Redis 独有，Memcached 和 DynamoDB 都有；常见补救是客户端本地缓存、键副本和读副本。
