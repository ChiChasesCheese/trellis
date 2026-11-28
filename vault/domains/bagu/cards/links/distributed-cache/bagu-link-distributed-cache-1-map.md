---
id: bagu-link-distributed-cache-1-map
node: links.distributed-cache
type: qa
step: 1
---
## Q
**分布式缓存（Redis） · 会被追问哪些八股**｜必会

设计分布式缓存（Redis）时，面试官最可能从哪几步下钻到基础知识？每一步问什么，怎么答？

## A
**基本回答。** 缓存节点内部和集群两层。基础是：单线程与事件循环、渐进式 rehash、淘汰策略、持久化的 fork、主从哨兵 Cluster 的高可用与丢写、哈希槽分片、热 key。

**下钻路线。**
- Redis 6.0 多线程改了什么 → I/O 线程只管 socket，命令仍单线程，扩容靠分片，[[a.redis.single-thread-fast|Redis 单线程为什么快]]
- 内存满了怎么办 → maxmemory-policy，缓存用 allkeys-lru 或 lfu，锁和幂等标记放 noeviction 实例，[[a.redis.expire-eviction|过期键删除与内存淘汰]]
- O(1) 的 LRU 怎么写 → 哈希表加双向链表，[[b.cache.lru|LRU 缓存的实现]]
- 做备份会不会影响线上 → fork 的写时复制放大内存，控制实例大小、在从库备份，[[a.redis.rdb-aof|RDB、AOF 与混合持久化]]
- 怎么做高可用 → 主从、哨兵、Cluster 分层，异步复制切换会丢最后几条写，[[a.redis.ha-overview|主从、哨兵与 Cluster 怎么保证高可用]]
- 怎么分片扩容 → 一致性哈希加虚拟节点；Redis Cluster 用 16384 个哈希槽，[[b.redis.cluster-slots|Redis Cluster 的哈希槽与重定向]]
- 主挂了会丢数据吗 → 异步复制会丢，WAIT 只缩小窗口，不保证强一致，[[b.scenario.distributed-kv|分布式 KV / 分布式缓存 / 文件存储设计]]
- 某个 key 太热，扩容也没用 → 本地缓存或复制 key，读能分摊，写不能，[[a.cache.hot-key|热 key 的发现与处理]]

**业务场景。** 余额缓存和幂等标记放缓存：主从切换会丢最近的写，所以幂等判断要有数据库唯一键兜底，锁和标记放不淘汰的独立实例。
**系统设计。** [[links.tt-cache-consistency-hot-keys|缓存一致性与热点 Key]]：那里讲读写路径与失效，这里讲节点内部与集群；[[links.url-shortener-design|短链接服务（URL Shortener / TinyURL）]]：缓存的用法同源，但数据几乎不修改。
