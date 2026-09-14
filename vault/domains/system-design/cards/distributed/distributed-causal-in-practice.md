---
id: distributed-causal-in-practice
node: distributed.consistency
type: qa
---
## Q
Causal consistency is theoretically the sweet spot — the strongest model that stays available under partition — yet almost no mainstream database offers it as a mode. Why not, and what do production systems use to get "causal enough" behavior?

## A
Why it's rare:
- **Tracking causality is expensive**: the system must know, for every write, which prior reads/writes it depends on — version vectors or dependency lists that grow with concurrency and must travel on every message and be checked before applying a write.
- **Dependencies snowball**: a write technically "depends on" everything its transaction read; safe over-approximation means large waits, precise tracking means intrusive APIs.

What's used instead:
- **Single-leader ordering as a free upgrade**: one leader's log totally orders all writes to a partition, which *implies* causal order within it — most systems get per-key or per-shard causality this way without any tracking.
- **Partition by causal domain**: put everything that must stay ordered (one user, one conversation) in one partition — cross-partition causality is then rare enough to ignore.
- **Session guarantees** (pin a client to a replica, or track its last-seen position/timestamp) — e.g. MongoDB causal sessions, Cosmos DB session level: causality for *your own* actions, which covers most UX bugs.

## Q zh
因果一致性（causal consistency）在理论上是甜点位——分区期间仍能保持可用的最强模型——但几乎没有主流数据库把它做成一个可选模式。为什么？生产系统用什么来获得"够用的因果"行为？

## A zh
它罕见的原因：
- **追踪因果关系很贵**：系统必须知道每个写依赖哪些先前的读/写——version vector 或依赖列表会随并发度增长，要随每条消息传输，并在应用写之前逐一校验。
- **依赖会滚雪球**：一个写在技术上"依赖"其事务读过的一切；安全的过度近似意味着大量等待，精确追踪则意味着侵入式的 API。

实际采用的替代：
- **单 leader 定序当免费升级**：一个 leader 的日志给分区内所有写一个全序，这在分区内*蕴含*了因果序——大多数系统靠这个免追踪地得到 per-key 或 per-shard 的因果性。
- **按因果域分区**：把必须保序的东西（同一个用户、同一段会话）放进同一个分区——跨分区的因果关系就稀少到可以忽略。
- **会话保证**（把客户端钉在一个副本上，或跟踪它最后看到的位点/时间戳）——如 MongoDB 的 causal session、Cosmos DB 的 session 级别：只对*你自己*的操作保证因果，这已覆盖大部分用户体验层面的 bug。
