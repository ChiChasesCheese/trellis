---
id: bagu-link-tt-cache-consistency-hot-keys-1-map
node: links.tt-cache-consistency-hot-keys
type: qa
step: 1
---
## Q
**缓存一致性与热点 Key · 会被追问哪些八股**｜必会

设计缓存一致性与热点 Key时，面试官最可能从哪几步下钻到基础知识？每一步问什么，怎么答？

## A
**基本回答。** 缓存让一份数据变成两份会分叉的副本。基础是：先更库再删缓存的时序、删除失败的兜底链路、从库延迟、击穿穿透雪崩三种失效、热 key 的本地缓存，以及锁只做优化。

**下钻路线。**
- 为什么不直接更新缓存 → 先更库再删缓存，并发写更新缓存会留下旧值，[[a.cache.db-consistency|缓存与数据库怎么保持一致]]
- 删除失败怎么办 → 应用重试，入 MQ 重试，订阅 binlog 再删一次，TTL 兜底，[[b.search.mysql-es-sync|MySQL 到 ES 的数据同步]]
- 回填读了落后的从库 → 刚失效的 key 读主库，或延迟双删，或带版本号比较，[[b.mysql.replication-lag|读写分离、主从延迟与读到旧数据]]
- 热 key 过期瞬间 → 互斥重建、逻辑过期、进程内合并回源，[[b.cache.breakdown|缓存击穿]]
- 查不存在的 ID → 布隆过滤器加空值缓存，[[a.cache.penetration|缓存穿透]]
- 大批 key 同时失效 → TTL 加随机抖动，多级缓存，限流降级，[[b.cache.avalanche|缓存雪崩]]
- 一个 key 二十万 QPS → 本地缓存一秒，再不够就复制 key，[[a.cache.hot-key|热 key 的发现与处理]]
- 重建缓存要不要加锁 → 带 TTL 的 Redis 锁即可，正确性互斥不能靠它，[[a.distributed.lock-redis-setnx|用 Redis 实现分布式锁]]

**业务场景。** 秒杀商品改价后详情页还显示旧价：展示可以容忍秒级旧值，但下单校验价格必须绕过缓存读主库。
**系统设计。** [[links.distributed-cache|分布式缓存（Redis）]]：那里讲缓存节点内部（淘汰、持久化、分片），这里讲读写路径的一致性；[[links.url-shortener-design|短链接服务（URL Shortener / TinyURL）]]：同样的穿透与热点，但数据几乎不修改。
