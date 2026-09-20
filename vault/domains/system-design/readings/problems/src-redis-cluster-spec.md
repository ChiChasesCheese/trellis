---
nodes: [problems.foundations.key-value-store, problems.foundations.distributed-cache]
url: https://redis.io/docs/latest/operate/oss_and_stack/reference/cluster-spec/
tags: [docs]
---
# Redis cluster specification
值得读：Redis 官方一手文档，给出了和 Dynamo 完全不同的分区与一致性哲学——固定 16384
个哈希槽（而不是一致性哈希环）、异步复制加"最后一次故障转移获胜"（而不是 vector clock
合并）、用 `MOVED`/`ASK` 客户端重定向代替服务端代理转发。两道题解都引用了它：键值存储
题解用它做一致性哲学的对照样本（严格 quorum/vector clock vs 异步复制/last-failover-wins
的取舍差异）；分布式缓存题解用它作为 Redis Cluster 分片、resharding 和故障转移机制本身
的一手依据。

%% trellis:begin %%
## Source
[Open the original ↗](https://redis.io/docs/latest/operate/oss_and_stack/reference/cluster-spec/)

## Archived copy
![[src-redis-cluster-spec-clip]]
%% trellis:end %%
