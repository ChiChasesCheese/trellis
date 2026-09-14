---
id: warehouse-cache-warms-automatically
node: cache.warehouse-local-disk-cache
type: qa
source: snowflake-docs
---
## Q
使用仓库本地 SSD 缓存需要用户手动配置要缓存哪些表或预热吗？

## A
不需要。这个缓存完全自动运作：只要仓库在运行，它就会自动缓存查询过程中访问到的表数据；仓库刚恢复运行时缓存是空的，随着仓库不断处理更多查询、访问更多数据，缓存会自然被重新填满并重建，用户无需任何手动干预。
