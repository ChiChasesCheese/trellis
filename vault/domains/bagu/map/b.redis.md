%% trellis:begin %%
# Redis
*B 其余知识点*

Redis 数据结构、持久化、高可用与线上用法；分布式锁单独放在「分布式基础」。

## Topics
- [[domains/bagu/map/b.redis.encodings|五种基本类型的底层编码（Object Encoding）]]
- [[domains/bagu/map/b.redis.hashtable-rehash|Redis 哈希表与渐进式 rehash（Incremental Rehash）]]
- [[domains/bagu/map/b.redis.listpack|压缩列表与 listpack：连锁更新（Cascade Update）]]
- [[domains/bagu/map/b.redis.replication-sync|主从复制：全量同步、增量同步与复制缓冲区]]
- [[domains/bagu/map/b.redis.sentinel-failover|哨兵选主、故障转移与脑裂（Sentinel, Split Brain）]]
- [[domains/bagu/map/b.redis.cluster-slots|Redis Cluster 的哈希槽与重定向（Hash Slot, MOVED/ASK）]]
- [[domains/bagu/map/b.redis.tx-lua-pipeline|Redis 事务、Lua 脚本与 Pipeline]]
- [[domains/bagu/map/b.redis.keys-scan|KEYS 与 SCAN：线上为什么不能用 KEYS]]
- [[domains/bagu/map/b.redis.bitmap-hll-geo|Bitmap、HyperLogLog、Geo：海量去重、计数与签到]]
- [[domains/bagu/map/b.redis.key-design|Redis Key 与缓存结构怎么设计（Key Design）]]
- [[domains/bagu/map/b.redis.blocking-slow|Redis 变慢与阻塞的常见原因（含内存碎片）]]
- [[domains/bagu/map/b.redis.stream-delay-queue|Redis 做消息队列与延时任务（List/Pub-Sub/Stream、Redisson）]]
%% trellis:end %%

## Notes
