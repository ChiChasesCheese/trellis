---
id: problems-news-feed-read-write-ratio-drives-precompute
node: problems.social.news-feed
type: qa
step: 1
tags: [grown]
---
## Q
In a news feed design with 200M daily active users where each user opens the app 8 times a day and views 3 feed pages per session (4.8 billion feed reads/day) against 4 million posts/day, why does the resulting ~1,200:1 read-to-write ratio push the design toward precomputing timelines at write time rather than aggregating them on every read?

## A
At a 1,200:1 read-to-write ratio, a read-time aggregation strategy (fan-out on read) would repeat the same expensive 'merge all followees' posts' computation on every one of ~55,556 average feed-read QPS, while write-time precomputation (fan-out on write) does that merge work only once per post, amortized over the much smaller ~46 posts/second write rate. Paying the aggregation cost on the rare write instead of the frequent read is what makes the 1,200x traffic asymmetry affordable.

## Q zh
在一个信息流设计中，2 亿日活用户平均每天打开 App 8 次、每次会话浏览 3 页时间线（合计 48 亿次/天的时间线读取），对应每天 400 万条发帖，由此得到约 1,200:1 的读写比，为什么这个比例会把设计推向'写时预计算时间线'而不是'每次读时实时聚合'？

## A zh
在 1,200:1 的读写比下，如果采用读时聚合策略（fan-out on read），平均约 55,556 QPS 的每一次读请求都要重复一遍'合并所有关注对象最新帖子'这样昂贵的计算；而写时预计算（fan-out on write）只需要在每条帖子发布时做一次这个合并，分摊到小得多的约每秒 46 条的写入速率上。把聚合开销放在少见的写操作而不是频繁的读操作上，正是能够承受 1,200 倍流量不对称的关键。
