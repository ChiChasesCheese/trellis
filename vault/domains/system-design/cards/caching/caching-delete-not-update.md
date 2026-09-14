---
id: caching-delete-not-update
node: caching.invalidation
type: qa
---
## Q
On a DB write, why is *deleting* the cache key generally safer than *updating* it with the new value?

## A
Concurrent updates race: two writers can update the DB in one order and the cache in the opposite order, leaving the cache holding the **older value indefinitely** (until TTL, if any).

Delete-on-write makes the next reader repopulate from the DB, so the worst case is one extra miss instead of a persistent wrong value. Remaining race (read miss loads old value while a write lands) is narrow and bounded by TTL — which is why you keep a TTL even with explicit invalidation.

## Q zh
在 DB 写入时，为什么 *删除* 缓存键通常比 *更新* 它为新值更安全？

## A zh
并发更新竞争：两个写者可以按一个顺序更新 DB 并按相反的顺序更新缓存，使缓存保持 **更旧的值无限期**（直到 TTL，如果有的话）。

写入时删除使下一个读者从 DB 重新填充，所以最坏的情况是一个额外的 miss 而不是持久的错误值。剩余竞争（读 miss 在写登陆时加载旧值）是狭窄的并由 TTL 界定 — 这就是为什么即使有明确的失效你也保持 TTL。
