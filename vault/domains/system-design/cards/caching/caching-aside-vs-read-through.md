---
id: caching-aside-vs-read-through
node: caching.strategies
type: qa
---
## Q
Cache-aside and read-through both populate the cache on a miss. What actually differs, and when does that difference matter?

## A
**Who owns the load logic.** In cache-aside the *application* checks the cache, fetches from the DB on miss, and writes the cache; in read-through the *cache layer* fetches from the store itself.

- Cache-aside: works with any dumb cache (Redis/Memcached), app can cache arbitrary computed shapes, but every service duplicates the load logic.
- Read-through: centralizes loading (e.g., a caching library or proxy with a loader), enables built-in coalescing of concurrent misses, but ties the cached shape to the store's data model.

## Q zh
Cache-aside 和 read-through 都在 miss 时填充缓存。实际上有什么不同，什么时候这种差异很重要？

## A zh
**谁拥有加载逻辑。** 在 cache-aside 中 *应用* 检查缓存，在 miss 时从 DB 获取，并写入缓存；在 read-through 中 *缓存层* 从存储中自己获取。

- Cache-aside：适用于任何哑缓存（Redis/Memcached），应用可以缓存任意计算形状，但每个服务都复制加载逻辑。
- Read-through：集中加载（例如，一个缓存库或带 loader 的代理），启用并发 miss 的内置合并，但将缓存形状绑定到存储的数据模型。
