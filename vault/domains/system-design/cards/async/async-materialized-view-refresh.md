---
id: async-materialized-view-refresh
node: async.streaming.processing
type: qa
---
## Q
You keep a denormalized read model (search index, cache, analytics table) fed from a change stream. How do you (a) keep it fresh and (b) fix it when it's wrong?

## A
- **Fresh**: a stream consumer applies each change; freshness = consumer lag, which you monitor as *lag age* (seconds behind), not message count. Writes must be idempotent (upsert keyed by entity id + version) because the stream is at-least-once.
- **Wrong**: don't patch it — **rebuild by replay**: reprocess the log from the start (or from a snapshot) into a new view, then cut reads over. This is the payoff of keeping the log as source of truth: derived data is disposable.

## Q zh
你保留一个去规范化的读模型（搜索索引、缓存、分析表），由变化流供给。如何（a）保持新鲜和（b）修复它当它错误时？

## A zh
- **新鲜**：stream consumer 应用每个变化；新鲜度 = consumer lag，你将其监控为*lag age*（秒数延迟），不是消息计数。写必须是幂等的（由 entity id + version keyed 的 upsert），因为流是 at-least-once。
- **错误**：不要修补它 — **通过重放重建**：从开始（或从快照）重新处理日志到新视图，然后切换读。这是保持日志作为真实来源的回报：派生数据是可任意处理的。
