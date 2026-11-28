---
id: bagu-link-realtime-game-leaderboard-1-map
node: links.realtime-game-leaderboard
type: qa
step: 1
---
## Q
**在线游戏排行榜（全球榜 + 我的名次 + 好友榜） · 会被追问哪些八股**｜必会

设计在线游戏排行榜（全球榜 + 我的名次 + 好友榜）时，面试官最可能从哪几步下钻到基础知识？每一步问什么，怎么答？

## A
**基本回答。** 排行榜是按分数有序集合上的名次查询。基础是：ZSet 与跳表的对数复杂度、单 key 在集群里只落一个槽、同分编码、热点读分流，榜单可由数据库重建。

**下钻路线。**
- 全球榜加我的名次 → ZINCRBY、ZREVRANGE、ZREVRANK 都是对数级；好友榜读时再算，[[a.scenario.like-leaderboard|点赞计数与实时排行榜]]
- 为什么 ZSet 用跳表、同分怎么排 → 跨度算排名；时间戳打包进分数，[[a.redis.zset-skiplist|ZSet 与跳表]]
- 榜单是一个 key，集群怎么分 → 单个 ZSet 只落一个槽，按分数段拆分，各取 Top-K 归并，[[b.redis.cluster-slots|Redis Cluster 的哈希槽与重定向]]
- 头部分页被所有人读 → 副本加随机读，或短 TTL 本地缓存，[[a.cache.hot-key|热 key 的发现与处理]]
- 同一玩家两次分数乱序 → 同 key 同分区，幂等生产者，[[a.mq.ordering|消息顺序性怎么保证]]
- Redis 重启榜单丢了 → RDB 或 AOF 加从库，真相仍在数据库可重建，[[a.redis.rdb-aof|RDB、AOF 与混合持久化]]

**业务场景。** 抖音直播间礼物榜：榜单是展示用的派生视图，Redis 丢了就用账务流水重建，不能反过来拿榜单当账。
**系统设计。** [[links.top-k-counts|Top-K 热门榜（视频播放、歌曲、话题标签）]]：同样排序，但窗口滑动、基数巨大要近似；[[links.tt-live-gift-coin-settlement|直播虚拟礼物：金币记账与主播结算]]：礼物榜只是展示，金币账务才是真相。
