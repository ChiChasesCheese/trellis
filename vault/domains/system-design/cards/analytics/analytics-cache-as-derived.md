---
id: analytics-cache-as-derived
node: analytics.derived
type: qa
---
## Q
Reframe cache invalidation as a derived-data problem. What does the reframing buy you over app-managed invalidation?

## A
A cache entry is a **materialized view of a query**; "invalidation" is just view maintenance. Instead of application code remembering to delete keys on every write path (dual-write: miss one path or crash mid-way and the cache lies indefinitely), subscribe a maintainer to the database's **change log (CDC)** and update/evict affected keys from there.

Buys you:
- **Completeness**: every committed write reaches the cache exactly once, in log order — no forgotten code path.
- **Rebuildability**: cold cache or bad entries? Replay/backfill like any derived view.

TTLs remain as the backstop bounding staleness when the pipeline breaks, not the primary mechanism.

## Q zh
将缓存失效重新框架化为派生数据问题。重新框架化对应用管理失效买了什么？

## A zh
缓存条目是**查询的物化视图**；"失效"只是视图维护。而不是应用代码记住在每个写路径上删除 key（dual-write：错过一个路径或在中途崩溃，缓存永远说谎），订阅维护器到数据库的**变化日志（CDC）**并从那里更新/驱逐受影响的 key。

买你：
- **完整性**：每个提交的写精确一次到达缓存，按日志顺序 — 没被遗忘的代码路径。
- **可重建性**：冷缓存或坏条目？像任何派生视图一样重放/回填。

TTL 保持为backstop，限制管道破裂时的陈旧度，不是主要机制。
