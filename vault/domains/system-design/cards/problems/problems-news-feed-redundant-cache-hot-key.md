---
id: problems-news-feed-redundant-cache-hot-key
node: problems.social.news-feed
type: qa
step: 3
tags: [grown]
---
## Q
In a news feed system, why doesn't adding more shards to a post-content cache fix the read-side hot key problem when a single post from a high-follower account goes viral and millions of users request the same post_id within seconds?

## A
Sharding by post_id always routes every request for that one viral post_id to the same single shard, regardless of how many total shards exist — adding shards only spreads load for keys that are actually distributed across different post_ids, not for repeated requests to one hot key. The fix is a redundant/replicated cache: the hot post's content is copied to N independent cache instances, and reads are routed by request identity (e.g. a random value or requesting user id) rather than by post_id, spreading the hot key's traffic evenly across all N replicas at the cost of each replica independently missing to the database once.

## Q zh
在一个信息流系统中，当某个高粉丝账号的一条帖子爆红、数百万用户在几秒内并发请求同一个 post_id 时，为什么给帖子内容缓存加更多分片解决不了这种读侧热点（hot key）问题？

## A zh
按 post_id 分片时，无论总共有多少分片，这一个爆红 post_id 的全部请求永远都会被路由到同一个分片——增加分片数只能分散那些真正分布在不同 post_id 上的负载，对重复请求同一个热 key 毫无帮助。正确做法是冗余/复制缓存（redundant/replicated cache）：把热帖内容复制到 N 个互相独立的缓存实例上，读请求按请求本身的身份（例如一个随机值或请求用户的 id）而不是按 post_id 路由，代价是每个副本各自要向数据库回源一次，换来的是热 key 的流量均匀摊到全部 N 个副本上。
