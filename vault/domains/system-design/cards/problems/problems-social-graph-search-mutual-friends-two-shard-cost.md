---
id: problems-social-graph-search-mutual-friends-two-shard-cost
node: problems.social.social-graph-search
type: qa
step: 2
tags: [grown]
---
## Q
In a social graph where the edge store is hash-partitioned by user id (so each user's roughly 300 direct connections could be spread across many different shards), why is a 'mutual friends between user A and user B' query cheap — touching only 2 shards — regardless of how many shards the partitioning scheme uses overall?

## A
The query only needs the full adjacency list of A (one single-shard fetch, since all of A's edges live on A's own shard by definition of the partitioning scheme) and the full adjacency list of B (one single-shard fetch on B's shard), then a local set intersection of the two roughly-300-element lists, which is cheap (on the order of a few hundred comparisons). The number of shards touched is bounded by the number of distinct users named in the query (2), not by how many shards those users' individual friends happen to be scattered across — that fan-out only becomes a problem for a different query, like generating friend-of-friend candidates.

## Q zh
在一个按用户 id 哈希分片的社交关系图存储里（一个用户约 300 个直接连接可能散落在很多不同的分片上），为什么「查询用户 A 和用户 B 的共同好友」很便宜——只需要 touch 2 个分片——而与分片方案总共用了多少个分片无关？

## A zh
这个查询只需要取到 A 的完整邻接表（一次单分片读取，因为按分片方案的定义，A 的全部边都在 A 自己所在的分片上）和 B 的完整邻接表（在 B 所在分片上的一次单分片读取），然后对这两个各约 300 个元素的集合做一次本地求交（大约几百次比较，很便宜）。查询要 touch 的分片数由查询里点名的用户数（2 个）决定，而不是由这些用户各自的好友散落在多少个分片上决定——后者的扇出只在另一类查询（比如生成好友的好友候选集）里才会成为问题。
