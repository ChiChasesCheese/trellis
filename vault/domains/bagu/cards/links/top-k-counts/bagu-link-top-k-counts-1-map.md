---
id: bagu-link-top-k-counts-1-map
node: links.top-k-counts
type: qa
step: 1
---
## Q
**Top-K 热门榜（视频播放、歌曲、话题标签） · 会被追问哪些八股**｜必会

设计Top-K 热门榜（视频播放、歌曲、话题标签）时，面试官最可能从哪几步下钻到基础知识？每一步问什么，怎么答？

## A
**基本回答。** 难在基数大、写入猛、窗口滑动。基础是：本机累加再批量写、无淘汰的内存 Map 就是泄漏、ZSet 取榜、时间桶合并窗口、局部 Top-K 再归并。

**下钻路线。**
- 播放计数怎么扛高并发 → 本机 LongAdder 累加再批量写 Redis，不能 volatile 自增，[[b.runtime.java-volatile-cas-jmm|volatile、CAS 与 Java 内存模型]]
- 内存里每个视频一个计数，key 无限增长 → 要淘汰或近似算法限内存，[[a.linux.mem-oom|内存占用高与 OOM 怎么查]]
- 名次查询为什么是对数级 → 随机层数加跨度累加，百万成员约 10 层，[[a.redis.zset-skiplist|ZSet 与跳表]]
- 近一小时、一天、一周的热门 → 时间桶聚合，窗口榜合并桶，桶 TTL 滚动，[[a.scenario.like-leaderboard|点赞计数与实时排行榜]]
- 离线精确 Top K，流式近实时怎么办 → 分桶统计加小顶堆归并；流式改用 Count-Min Sketch 加堆，[[b.scenario.massive-data-topk|海量数据]]
- 热门内容缓存淘汰用 LRU 还是 LFU → 一次性扫描会挤掉热数据，LFU 抗扫描，[[a.redis.expire-eviction|过期键删除与内存淘汰]]
- Redis 挂了榜单怎么办 → 本地缓存，降级返回旧榜，[[b.cache.avalanche|缓存雪崩]]
- 离线补算每个话题前 N 视频 → 按话题分区、播放量倒序编号取前 N，[[b.mysql.sql-handwrite|SQL 手撕与常见写法]]

**业务场景。** 抖音热点话题的播放事件每秒暴涨：写入先在本机聚合再批量落榜，读榜走缓存，不能让每次读都去重算。
**系统设计。** [[links.realtime-game-leaderboard|在线游戏排行榜（全球榜 + 我的名次 + 好友榜）]]：玩家榜要精确名次，热门榜只要前 K 且允许近似；[[links.ad-click-aggregator|广告点击聚合]]：同样的写入预聚合，输出是按广告的计数。
