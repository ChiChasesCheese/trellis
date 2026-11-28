---
id: hi-c-sd-caching-n02-external
node: sd.core-concepts.caching.notes
type: qa
step: 2
---
## Q
**缓存 · 缓存放在哪里 · 外部缓存**｜摘要 · 必会
Redis、Memcached 这种外部缓存是什么？为什么它是面试里的默认答案？

## A
- **是什么：** 一个独立的缓存服务，应用通过网络访问，把常读的数据放进去，避免每次都查数据库。
- **优点：** 所有应用实例共享同一份缓存，所以规模变大时命中率不会被实例数稀释；支持淘汰策略（如 LRU）和过期时间（TTL），内存占用可控。
- **面试用法：** 凡是高流量系统都先说外部缓存（Redis）；CDN、客户端缓存是在题目需要时再叠加的层。
- **2026 亮点：** 选引擎时可以提许可证：Redis 2024 年改为 RSALv2/SSPLv1，Redis 8 又加回 AGPLv3 选项；Valkey 与 Redis 协议兼容，ElastiCache 已提供且比同类引擎便宜（Serverless 低 33%、节点型低 20%）。按许可证合规、云厂商支持和所需新特性选，不必一律默认 Redis。
