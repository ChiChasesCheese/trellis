---
id: problems-news-feed-10x-physical-shard-inbox
node: problems.social.news-feed
type: qa
step: 8
tags: [grown]
---
## Q
In a news feed design scaling from 200M to 2 billion daily active users (a 10x jump), why does the inbox cache need to move from a single Redis cluster to multiple physically isolated clusters sharded by user_id, rather than just adding more nodes to one cluster?

## A
At 200M users with an 800-entry cap and ~20 bytes/entry, the inbox cache totals about 3.2TB; at 10x the user count it grows to about 32TB, which is beyond what a single cluster can reasonably hold or fail over as one unit. Sharding physically by user_id into multiple independent clusters bounds the blast radius of any single cluster's failure to the users it owns, and lets each cluster be scaled, upgraded, or recovered independently — the same isolation principle as partitioning a single hot resource (like one event's seat inventory) away from unrelated traffic, rather than trusting one ever-growing cluster to absorb unlimited scale.

## Q zh
在一个信息流设计从 2 亿日活扩展到 20 亿日活（10 倍增长）的场景下，为什么收件箱缓存需要从单一 Redis 集群改为按 user_id 物理隔离的多个独立集群，而不是简单地往一个集群里加更多节点？

## A zh
在 2 亿用户、800 条上限、每条约 20 字节的假设下，收件箱缓存总量约 3.2TB；用户数增长 10 倍后会增长到约 32TB，这已经超出单一集群能合理承载或作为一个整体做故障转移的规模。按 user_id 物理拆分成多个独立集群，能把任何一个集群故障的影响范围限制在它所负责的那部分用户内，并让每个集群可以独立扩容、升级、恢复——这和把单一热点资源（比如某一场演出的座位库存）与无关流量隔离开是同一个隔离原则，而不是寄希望于一个不断膨胀的单一集群能无限吸收增长。
