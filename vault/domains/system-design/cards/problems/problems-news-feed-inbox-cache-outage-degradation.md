---
id: problems-news-feed-inbox-cache-outage-degradation
node: problems.social.news-feed
type: qa
step: 7
tags: [grown]
---
## Q
In a news feed system, what is the correct degradation behavior when the inbox cache (the Redis-class store holding each user's precomputed home timeline) becomes unavailable, and why is this better than returning an error?

## A
The correct degradation is to fall back to real-time fan-out on read: reconstruct the requesting user's timeline by fetching recent posts directly from each followee's post store and merging them on the fly, instead of reading the precomputed inbox. This is strictly slower (latency degrades from sub-200ms to the second range) but keeps the feed functional, because the inbox cache is a materialized view that can always be rebuilt from the authoritative post store and follow graph — it is not the source of truth, so its unavailability should degrade performance, not correctness or availability.

## Q zh
在一个信息流系统中，当收件箱缓存（保存每个用户预计算主时间线的 Redis 类存储）不可用时，正确的降级行为是什么？为什么这比直接返回错误更好？

## A zh
正确的降级是退化为实时的读时 fan-out：直接从每个被关注对象的帖子存储里拉取最新帖子并即时合并，重建请求用户的时间线，而不是去读预计算的收件箱。这样做延迟明显变差（从亚 200ms 劣化到秒级），但信息流功能依然可用，因为收件箱缓存只是一份可以随时从权威的帖子存储和关注关系图重建出来的物化视图，不是数据的权威来源——它的不可用应该只影响性能，不应该影响正确性或整体可用性。
