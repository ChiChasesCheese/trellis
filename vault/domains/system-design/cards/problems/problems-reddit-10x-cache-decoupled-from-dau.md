---
id: problems-reddit-10x-cache-decoupled-from-dau
node: problems.social.reddit
type: qa
step: 8
tags: [grown]
---
## Q
In a forum design whose hot-listing cache is sized by (number of communities × entries per community) rather than by user count, what specifically breaks at 10x DAU growth (100M to 1B), and what does NOT break?

## A
The hot-listing cache itself barely grows — it stays roughly the same size unless the number of communities also grows, since DAU doesn't appear in its sizing formula. What does break is everything sized by write volume: vote, comment, and post throughput all grow roughly with DAU, so the vote ledger and comment store both need more shards, and any individual community whose own write QPS now exceeds a single shard's capacity needs to be physically isolated onto a dedicated shard, the same way an extreme single-target vote hot key gets split into sub-counters.

## Q zh
在一个热门列表缓存大小由（社区数量 × 每社区条目数）而不是用户数决定的论坛设计里，日活涨 10 倍（1 亿到 10 亿）时，具体什么会出问题？什么不会？

## A zh
热门列表缓存本身几乎不会变大——只要社区数量不同步增长，它的大小基本不变，因为日活根本不出现在它的容量公式里。会出问题的是一切按写入量计算的部分：投票、评论、发帖的吞吐都大致随日活增长，所以投票账本和评论存储都需要增加分片；任何单个社区自身的写 QPS 一旦超出单个分片的承受能力，就需要把它物理隔离到专属分片上，和极端情况下把单一目标的投票计数器拆成子计数器是同一种思路。
