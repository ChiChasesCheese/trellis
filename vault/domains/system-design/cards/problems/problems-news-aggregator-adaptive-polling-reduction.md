---
id: problems-news-aggregator-adaptive-polling-reduction
node: problems.search.news-aggregator
type: qa
step: 1
tags: [grown]
---
## Q
In a news aggregator design polling hundreds of thousands of publisher RSS feeds, why does a single fixed polling interval applied to every publisher waste most of its request budget, and what does adapting each feed's poll interval to its own observed update frequency achieve?

## A
Publisher update frequency follows a power-law-like distribution: a small fraction of high-frequency wire-service sources update every few minutes, while the long tail of feeds updates every few days, so a single interval tuned for the average either polls quiet long-tail feeds far more often than they ever change (wasted requests) or polls high-frequency feeds too rarely to catch breaking updates. Setting each feed's poll interval from its own observed update interval (clamped to a min/max range) concentrates request budget where content actually changes. In a worked example with 300,000 publishers split into a 5% high-frequency tier, 20% daily tier, and 75% long-tail tier, adaptive polling drops total polling load from 1,000 requests/sec (uniform 5-minute interval) to about 141 requests/sec — roughly a 7.1x reduction.

## Q zh
在一个轮询几十万个发布方 RSS 源的新闻聚合器设计中，为什么对所有发布方使用同一个固定轮询间隔会浪费大部分请求预算？把每个源的轮询间隔按自己观测到的更新频率自适应调整能带来什么？

## A zh
发布方更新频率近似服从幂律分布：一小部分高频通讯社类源每几分钟更新一次，而长尾的大部分源每几天才更新一次，所以按平均值统一设置的间隔要么对几乎不变的长尾源过度轮询（浪费请求），要么对高频源轮询不够频繁而错过突发更新。把每个源的轮询间隔按自己观测到的更新间隔设置（限制在一个最小/最大范围内），能把请求预算集中在真正有内容变化的地方。在一个具体算例中，30 万个发布方按 5% 高频层、20% 日更层、75% 长尾层划分，自适应轮询把总轮询负载从统一 5 分钟间隔的 1,000 请求/秒降到约 141 请求/秒——降低约 7.1 倍。
