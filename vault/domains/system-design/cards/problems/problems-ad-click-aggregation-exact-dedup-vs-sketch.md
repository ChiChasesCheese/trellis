---
id: problems-ad-click-aggregation-exact-dedup-vs-sketch
node: problems.search.ad-click-aggregation
type: qa
step: 2
tags: [grown]
---
## Q
In an ad click aggregation design, why must click deduplication use an exact key-value store rather than a probabilistic structure like a Bloom filter or Count-Min Sketch, even though such structures would use far less memory?

## A
Deduplication is a binary decision — does this click count for billing or not — and a probabilistic structure's false positive (wrongly treating a genuinely new click as a duplicate) silently and permanently discards a real, billable event with no way to recover which one was dropped from the summary itself. That's a fundamentally different failure than a heavy-hitters sketch's error, where a count being off by a bounded amount doesn't change which items are considered popular. Because deduplication decides whether money changes hands, it needs an exact existence check (e.g. a keyed store like RocksDB) even at the cost of more memory than a sketch would use.

## Q zh
在一个广告点击聚合设计中，为什么点击去重必须用精确的 key-value 存储，而不能用 Bloom filter 或 Count-Min Sketch 这类概率性结构，即便后者能省下大量内存？

## A zh
去重是一个二元判断——这次点击算不算计费——概率性结构的假阳性（把一次真实的新点击误判为重复）会悄无声息、且永久地丢掉一个真实的、本该计费的事件，而且没办法从摘要本身反推出丢的是哪一条。这和热门内容 sketch 的误差本质不同：后者计数偏差一点，并不改变「哪些内容算热门」这个结论。因为去重决定的是钱要不要转手，它需要一次精确的存在性检查（比如 RocksDB 这类 key-value 存储），哪怕比 sketch 多花内存也要用。
