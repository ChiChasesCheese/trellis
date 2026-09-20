---
id: problems-email-service-per-user-search-sharding-changes-problem
node: problems.media.email-service
type: qa
step: 5
tags: [grown]
---
## Q
A global search engine shards its corpus so any query typically fans out to multiple shards, with tail latency dominated by the slowest shard. A per-user email search index, where each user's mail is isolated by product semantics, can instead shard by user id so a query touches exactly one shard. Does this eliminate the sharding problem, or does it just change what kind of problem sharding has to solve — and what problem replaces fan-out/tail-latency?

## A
It changes the problem rather than eliminating it. Removing fan-out and tail-latency concerns doesn't remove the need for careful sharding — it replaces scatter-gather load balancing with a hot-shard problem: a small number of unusually large mailboxes (automation accounts, users who archive everything indefinitely) can hold far more index data than the typical mailbox, and if shards are assigned by a plain hash of user id, those outlier mailboxes concentrate disproportionate storage and query load onto whichever shard they land on. The fix is consistent hashing with virtual nodes plus a soft cap on how much index data a single shard holds, migrating the heaviest few mailboxes to dedicated shards once the cap is exceeded — a hot-entity problem, not the hot-key-on-a-single-viral-item problem a social feed's cache faces, and not the multi-shard-fan-out problem a shared-corpus search engine faces.

## Q zh
全局搜索引擎对语料分片后，一次查询通常需要扇出到多个分片，长尾延迟由最慢的分片决定。而一个按用户隔离语料的邮件搜索索引可以按 user_id 分片，让一次查询只落在唯一一个分片上。这是不是就消除了分片问题？还是说它只是把分片要解决的问题类型换掉了？换成了什么问题？

## A zh
它是把问题换掉了，而不是消除了。去掉扇出和长尾延迟的顾虑，并不意味着不再需要谨慎分片——它把「scatter-gather 负载均衡」问题换成了「热分片」问题：极少数异常庞大的邮箱（自动化脚本账号、无限期归档所有邮件的用户）持有的索引数据量远超普通邮箱，如果按 user_id 简单哈希分片，这些离群邮箱会把不成比例的存储和查询负载集中砸到它们所落的那一个分片上。解法是一致性哈希加虚拟节点，再对单个分片能持有的索引数据量设一个软上限，超出上限时把最重的少数邮箱迁移到专门的分片——这是一个「热实体」问题，既不同于社交信息流缓存里「单个爆款内容」那种热 key 问题，也不同于共享语料搜索引擎那种多分片扇出问题。
