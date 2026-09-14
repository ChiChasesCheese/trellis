---
id: warehouse-cache-dropped-on-suspend
node: cache.warehouse-local-disk-cache
type: qa
source: snowflake-docs
---
## Q
一个虚拟仓库在挂起（suspend）之后又被恢复（resume）运行，为什么恢复之后的最初几条查询往往会比挂起之前明显更慢？

## A
因为仓库挂起时会释放其所有计算资源，寄存在这些资源本地磁盘上的表数据缓存也随之被整体丢弃；仓库恢复运行后，这个缓存是空的，只有在仓库重新处理查询、逐步把访问过的数据再次缓存进去之后，后续查询才能重新享受到缓存带来的性能提升，所以恢复初期会出现一段冷启动式的性能下降。
