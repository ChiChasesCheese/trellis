---
id: caching-write-through-vs-behind
node: caching.strategies
type: qa
---
## Q
Write-through vs write-behind (write-back): what does each cost you, and what breaks in write-behind if the cache node dies?

## A
- **Write-through**: write goes to cache *and* store synchronously. Cost: every write pays store latency; cache is never fresher than needed. Safe but slow.
- **Write-behind**: write acks after hitting the cache; the store is updated asynchronously in batches. Cost: **acknowledged writes are lost** if the cache node crashes before flush, and the store lags so other readers see stale data.

Write-behind fits high-write, loss-tolerant data (counters, view stats) — never money or anything the store must durably own at ack time.

## Q zh
Write-through vs write-behind（write-back）：每个成本你什么，以及如果缓存节点死亡 write-behind 中什么会破坏？

## A zh
- **Write-through**：写入同步进入缓存 *和* 存储。成本：每次写入支付存储延迟；缓存永远不会比需要的新鲜。安全但慢。
- **Write-behind**：写入在命中缓存后确认；存储在批处理中异步更新。成本：**已确认的写入会丢失** 如果缓存节点在刷新前崩溃，存储滞后所以其他读者看到过时数据。

Write-behind 适合高写入、容损数据（计数器、查看统计） — 永远不是金钱或商店必须在确认时耐用拥有的任何东西。
