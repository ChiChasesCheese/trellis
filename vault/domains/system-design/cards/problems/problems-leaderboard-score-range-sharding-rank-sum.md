---
id: problems-leaderboard-score-range-sharding-rank-sum
node: problems.realtime.leaderboard
type: qa
step: 2
tags: [grown]
---
## Q
Once a leaderboard's write throughput has grown past what a single Redis primary can sustain and it must be sharded, answering "what's my global rank" requires knowing how many players across the whole leaderboard outrank you. Why does sharding by player id make this expensive, and what sharding key keeps it cheap?

## A
Sharding by player id spreads write load evenly, but it scatters players with similar scores across every shard at random, so computing a global rank requires scattering a query to every shard and merging the results — a cost that grows with the number of shards instead of shrinking with it. Sharding by score range instead keeps each shard responsible for a contiguous slice of the score distribution, and each shard maintains a cheap O(1) count of its own members. A player's global rank then becomes the sum of the member counts of every shard entirely above their score range, plus their local rank within their own shard — a sum over a small, fixed number of shards, independent of the total player count. This is worth doing only once sharding is actually needed for throughput; a single primary answers rank queries directly without any of this cross-shard bookkeeping.

## Q zh
一旦排行榜的写入吞吐超出了单个 Redis 主节点能撑住的范围、必须分片之后，回答「我的全球排名是多少」需要知道整个排行榜里有多少玩家分数比自己高。为什么按玩家 id 分片会让这件事变贵？什么样的分片键能让它保持便宜？

## A zh
按玩家 id 分片能让写入负载均匀分散，但它会把分数相近的玩家随机打散到每个分片里，于是计算全局排名需要向所有分片发起查询再合并结果——这个代价随分片数增长而变大，而不是变小。改成按分数区间分片，则每个分片只负责分数分布里连续的一段，每个分片维护自己成员数量的廉价 O(1) 计数。这样一名玩家的全局排名就等于「排在其分数区间之上的所有分片成员数之和」加上「他在自己分片内的本地排名」——这只是对固定的、少量分片求和，和总玩家数无关。这套机制只有在吞吐真的逼出分片时才值得引入；一个单一主节点可以直接回答排名查询，完全不需要这套跨分片的记账。
