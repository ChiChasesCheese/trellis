---
id: warehouse-cache-dropped-on-downsize
node: cache.warehouse-local-disk-cache
type: qa
source: snowflake-docs
---
## Q
把一个正在运行、且已经积累了不少缓存的仓库从 X-Large 缩小到 Large，除了减少计算资源和信用点（credit）消耗之外，还会带来什么容易被忽视的副作用？

## A
缩小规格会移除仓库中的一部分计算资源，而寄存在这些被移除资源本地磁盘上的那部分表数据缓存也会随之丢失；这与整体挂起仓库导致缓存全部丢失是同一种机制的局部版本，只是丢失的是被移除那部分资源上的缓存，因此缩小规格同样可能带来短期的性能下降，直到剩余资源重新积累起足够的缓存。
