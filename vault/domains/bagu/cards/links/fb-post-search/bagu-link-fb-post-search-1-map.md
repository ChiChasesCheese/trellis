---
id: bagu-link-fb-post-search-1-map
node: links.fb-post-search
type: qa
step: 1
---
## Q
**Facebook 帖子搜索 · 会被追问哪些八股**｜必会

设计Facebook 帖子搜索时，面试官最可能从哪几步下钻到基础知识？每一步问什么，怎么答？

## A
**基本回答。** 倒排索引加两种排序加写放大。基础是：倒排索引与准实时可见、写入同步、分片倾斜、ZSet 排序、多层缓存、点赞写放大削峰、LSM 存储。

**下钻路线。**
- 为什么搜索快、新帖多久可见 → 倒排索引，1 秒 refresh 的准实时，[[b.search.es-inverted-index|Elasticsearch 倒排索引、mapping 与查询执行]]
- 帖子怎么进索引 → 双写、定时同步或 CDC 订阅，CDC 最稳，[[b.search.mysql-es-sync|MySQL 到 ES 的数据同步]]
- 热门关键词分片倾斜 → 看分片大小与路由，热点拆分，[[b.search.es-cluster-skew|ES 集群分片、数据倾斜与生产部署]]
- 按点赞数排序 → 另建一份 ZSet 索引，[[a.redis.zset-skiplist|ZSet 与跳表]]
- 搜索读缓存 → Redis 加 CDN，两层存活时间要合起来算，[[b.cache.multilevel|多级缓存设计与冷启动]]
- 点赞远多于发帖 → Kafka 缓冲削峰，索引只在点赞数过 2 的幂时更新，[[b.mq.why-mq|为什么用消息队列]]
- 写多读少的存储 → LSM 追加写优于 B+ 树，[[b.search.lsm-vs-btree|LSM-Tree 与 B+ Tree 的本质区别]]
- 语义相近但没有关键词 → 再加向量召回做混合，[[b.agent.rag-vector-index|向量索引与向量数据库]]

**业务场景。** 抖音搜索视频：新发布一分钟内可搜；违规视频下架后，要立刻从索引和缓存中删除。
**系统设计。** [[links.news-aggregator-feed|新闻聚合系统（Google News）]]：同样按时间建索引，来源是外部出版商；[[links.top-k-counts|Top-K 热门榜（视频播放、歌曲、话题标签）]]：点赞与播放同样是写放大，输出的是榜单。
