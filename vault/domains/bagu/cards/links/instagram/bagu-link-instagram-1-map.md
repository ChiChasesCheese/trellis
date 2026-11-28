---
id: bagu-link-instagram-1-map
node: links.instagram
type: qa
step: 1
---
## Q
**图片分享（Instagram） · 会被追问哪些八股**｜必会

设计图片分享（Instagram）时，面试官最可能从哪几步下钻到基础知识？每一步问什么，怎么答？

## A
**基本回答。** 读多写多的 feed 加图片分发。基础是：CDN 与 HTTP/2、强缓存与内容哈希 URL、缓存雪崩与降级、游标翻页、大文件流式处理、binlog 主从。

**下钻路线。**
- 一屏几十张图怎么加载快 → CDN 加 HTTP/2 多路复用，弱网再考虑 HTTP/3，[[b.net.http-versions|HTTP/1.1、HTTP/2、HTTP/3 的差异]]
- 图片读多写少 → CDN 长强缓存，URL 带内容哈希，更新即换 URL，[[b.net.http-basics-cache|HTTP 基础]]
- 大图上传处理 → 流式分块，不能整个读进内存，否则 Full GC，[[a.runtime.java-gc-fullgc|JVM 垃圾回收]]
- 首页 feed 缓存同时失效 → TTL 加抖动，限流降级，返回稍旧的 feed，[[b.cache.avalanche|缓存雪崩]]
- 排序服务挂了 → 降级为时间序或旧 feed，功能分级 P0 / P1 / P2，[[b.protect.degrade|降级怎么做]]
- feed 翻页不重复 → 游标分页，不用 OFFSET，[[b.mysql.deep-pagination|深分页为什么慢、怎么优化]]
- 读压力大怎么优化 → 改写 SQL、索引、缓存、分库分表，代价递增，[[a.mysql.slow-sql-triage|一条 SQL 变慢怎么排查与优化]]
- 首页 feed 怎么生成 → 推拉结合，大 V 的帖子读时按时间归并，[[b.scenario.follow-feed|关注关系与 Feed 流]]

**业务场景。** 抖音首页封面和图文：热门封面走 CDN 长缓存，首页推荐缓存同一时刻整体失效时，要靠抖动和降级保护数据库。
**系统设计。** [[links.youtube|视频平台（YouTube）]]：同样靠 CDN，多了分段转码与自适应码率；[[links.news-aggregator-feed|新闻聚合系统（Google News）]]：同样的 feed 游标翻页，但内容来自外部出版商而不是关注关系。
