---
id: problems-news-aggregator-edition-cache-decouples-read-cost
node: problems.search.news-aggregator
type: qa
step: 7
tags: [grown]
---
## Q
In a news aggregator's read path, why can't per-request live re-ranking simply be replaced by 'invalidate the cache when a new article arrives,' the way a write-triggered cache invalidation might work elsewhere, and what does a periodic per-edition ranking cache do instead?

## A
A story's ranking score keeps drifting over time purely from the time-decay factor even when no new article arrives, so a cache that only invalidates on writes would still serve a score that's silently gone stale between writes. Instead, a background ranking worker recomputes each (region, language) edition's full ranked list on a short fixed cadence (e.g. every 60 seconds) and publishes it to a shared read cache keyed by edition rather than by user, since ranking is shared across every reader of that edition rather than personalized; read requests are served directly from this cache, decoupling read QPS entirely from ranking computation cost. The trade-off is a bounded, known staleness window (at most one refresh cycle) rather than perfect per-request freshness or an unbounded stale cache.

## Q zh
在一个新闻聚合器的读路径中，为什么不能简单地用「有新文章到达时才让缓存失效」这种写触发的缓存失效策略来代替每次请求现场重新排序？周期性的按版面排序缓存做了什么不同的事？

## A zh
一个故事的排序分数即使没有新文章到达，也会单纯因为时间衰减因子持续漂移，所以一个只在写入时才失效的缓存，在两次写入之间依然会悄悄返回一个已经过期的分数。取而代之的是，一个后台排序 worker 按固定的短周期（比如每 60 秒）为每个（地区、语言）版面重新计算完整排序列表，写入一个按版面而不是按用户分 key 的共享读缓存——因为排序结果是同版面所有读者共享的，不是个性化的；读请求直接从这个缓存返回，读 QPS 因此和排序计算成本完全解耦。代价是一个有界、已知的陈旧窗口（最多一个刷新周期），而不是完美的每请求实时性，也不是一个永不过期的陈旧缓存。
