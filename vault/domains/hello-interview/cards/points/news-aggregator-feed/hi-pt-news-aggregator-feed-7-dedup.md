---
id: hi-pt-news-aggregator-feed-7-dedup
node: qb.sd.news-aggregator-feed.points
type: qa
step: 7
---
## Q
**新闻聚合系统 · 同一新闻多家报道的去重聚类**｜必会 · 出自：新闻聚合系统 › 深入 3

转载和多家报道同一事件，怎么去重并在信息流里只展示一次？成本怎么控制？

## A
**精确。** 规范化 URL（去掉 `utm_*`）哈希，解决转载同链接。
**近似。** 对标题加前几百字做 simhash（海明距离 ≤ 3 视为同一故事）或 MinHash + LSH；命中已有簇就并入 `cluster_id`，只展示代表文章并附「另有 N 家报道」。
**成本。** 只与同分类、近 48 小时窗口内的簇比较，内存和计算有上界。
