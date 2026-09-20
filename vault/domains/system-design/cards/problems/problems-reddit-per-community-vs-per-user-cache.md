---
id: problems-reddit-per-community-vs-per-user-cache
node: problems.social.reddit
type: qa
step: 1
tags: [grown]
---
## Q
In a Reddit-style forum design with 100M DAU and about 150,000 active communities, a hot-listing cache holding the top 1,000 ranked posts per community (20 bytes/entry) totals about 3GB (9GB at 3x replication). Why is this roughly 1,000x smaller than the multi-terabyte per-user inbox cache used in a follow-based news feed design at similar user scale, and what does that imply about how the cache grows as the user base grows?

## A
A follow-based feed personalizes content per follower, so it needs one precomputed inbox per user — the cache scales with (users × entries per user). A forum's hot listing is shared: every subscriber of a community reads the same cached ranked list, so the cache scales with (communities × entries per community) instead, and the user count doesn't appear in that formula at all. The direct implication: growing DAU 10x barely changes this cache's size (it only grows if the number of communities grows), whereas a per-user inbox cache grows roughly linearly with DAU.

## Q zh
在一个 100M 日活、约 15 万个活跃社区的 Reddit 式论坛设计里，一份每社区保留前 1,000 条排名帖子（每条 20 字节）的热门列表缓存总共约 3GB（三副本 9GB）。为什么这比同等用户规模下、基于关注关系的信息流设计所用的、以 TB 计的按用户收件箱缓存要小约 1,000 倍？这对缓存随用户规模增长的方式意味着什么？

## A zh
基于关注关系的信息流按每个关注者个性化内容，所以需要为每个用户各存一份预计算收件箱——缓存大小是（用户数 × 每用户条目数）。论坛的热门列表是共享的：一个社区的全体订阅者读的是同一份缓存好的排序列表，所以缓存大小是（社区数 × 每社区条目数），公式里根本不出现用户数这一项。直接的推论是：日活涨 10 倍几乎不改变这份缓存的大小（只有社区数量增长才会让它变大），而按用户收件箱的缓存大小基本随日活线性增长。
