---
id: warehouse-cache-scales-with-size
node: cache.warehouse-local-disk-cache
type: qa
source: snowflake-docs
---
## Q
一个正在运行的虚拟仓库（virtual warehouse）会自动缓存它处理查询时读取过的表数据，为什么把仓库规格从 Small 升级到 X-Large 会让这个缓存变得更大、更有效？

## A
这个缓存是由仓库内的计算资源（本地磁盘/SSD）承载的，仓库规格越大，其拥有的计算资源就越多，能用来存放已扫描表数据的本地磁盘空间也就相应越大；所以更大的仓库不仅算力更强，也天然拥有更大的缓存容量，能让更多后续查询命中缓存而不必重新从远程存储读取数据。
