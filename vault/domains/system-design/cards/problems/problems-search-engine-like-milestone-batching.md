---
id: problems-search-engine-like-milestone-batching
node: problems.search.search-engine
type: qa
step: 6
tags: [grown]
---
## Q
In a search system that lets users sort results by like count, why does updating a separate like-count sort index only when a post's like count crosses a power-of-2 milestone (1, 2, 4, 8, 16, ...) instead of on every like event reduce write load so much more for a viral post than for an average one?

## A
The number of milestone updates for a post that eventually receives L likes is floor(log2(L)) + 1, versus L updates if every like triggered a write. For a viral post with 100,000 total likes, that's 17 milestone updates instead of 100,000 — a roughly 5,882x reduction. For an average post with only 8 likes, it's 4 updates instead of 8 — a modest 2x reduction. The savings scale with how concentrated the likes are, which means the mechanism pays off most exactly where the write pressure would otherwise be highest: viral posts receiving a burst of likes.

## Q zh
在一个允许用户按点赞数排序结果的搜索系统中，为什么只在帖子点赞数跨越 2 的幂次里程碑（1, 2, 4, 8, 16, …）时才更新一个独立的按点赞数排序索引，而不是每次点赞都更新，能给爆款帖子带来比普通帖子大得多的写入负载降低？

## A zh
一条最终获得 L 个赞的帖子，用里程碑方式只需要 ⌊log2(L)⌋+1 次索引更新，而不是每次点赞都触发写入的 L 次。一条最终获得 10 万个赞的爆款帖子，只需要 17 次里程碑更新而不是 10 万次——降低约 5,882 倍。一条只有 8 个赞的普通帖子，只需要 4 次更新而不是 8 次——降低幅度很有限（约 2 倍）。这个收益随点赞的集中程度增长，意味着这个机制恰恰在写入压力本该最大的地方（点赞集中爆发的爆款帖子）收益最大。
