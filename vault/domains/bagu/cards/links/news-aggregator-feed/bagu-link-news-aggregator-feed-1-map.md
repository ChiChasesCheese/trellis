---
id: bagu-link-news-aggregator-feed-1-map
node: links.news-aggregator-feed
type: qa
step: 1
---
## Q
**新闻聚合系统（Google News） · 会被追问哪些八股**｜必会

设计新闻聚合系统（Google News）时，面试官最可能从哪几步下钻到基础知识？每一步问什么，怎么答？

## A
**基本回答。** 读远多于写、写入被外部世界牵着走。基础是：游标翻页、按时间的索引分片与冷热分层、慢查询排查、对不可靠出版商熔断、热点分类的写入分流。

**下钻路线。**
- 信息流翻页时有新文章插入 → 用 (发布时间, id) 游标，不会错位重复，[[b.mysql.deep-pagination|深分页为什么慢、怎么优化]]
- 按发布时间建索引 → 最新分片成热点，rollover 控制大小并冷热分层，[[b.search.es-cluster-skew|ES 集群分片、数据倾斜与生产部署]]
- 大促列表接口 P99 暴涨 → 先分单条慢还是全慢，再看慢日志、EXPLAIN、锁，[[a.mysql.slow-sql-triage|一条 SQL 变慢怎么排查与优化]]
- 上线前怎么确认用上索引 → EXPLAIN 看 key_len 和 rows，[[a.mysql.leftmost-index-failure|联合索引、最左前缀与索引失效]]
- 某家出版商一直 5xx → 每家一个熔断器，指数退避拉长拉取间隔，[[b.protect.breaker|熔断器的三态与触发条件]]
- 突发新闻同一分类写入热点 → 摄取节点先在内存聚合再批量写，[[a.cache.hot-key|热 key 的发现与处理]]
- 同一篇文章被转载或更新 → 内容哈希去重，加版本字段，[[b.agent.rag-eval-update|RAG 评测与知识库更新]]

**业务场景。** 抖音热点榜遇到突发新闻时，同一话题短时间内涌入大量内容，写入要先聚合，读走缓存。
**系统设计。** [[links.instagram|图片分享（Instagram）]]：同样游标翻页，但内容来自关注关系；[[links.notification-system-scale|通知系统（支持单发与群发，百万级每秒）]]：突发新闻的推送走高优先级通道，与普通通知隔离。
