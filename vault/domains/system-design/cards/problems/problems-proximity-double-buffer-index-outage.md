---
id: problems-proximity-double-buffer-index-outage
node: problems.geo.proximity
type: qa
step: 7
tags: [grown]
---
## Q
In a proximity search system where the in-memory spatial index is rebuilt periodically and swapped in with double buffering, why is falling back to the last successfully loaded index snapshot a better degradation strategy than either returning an error or scanning the business database directly when a rebuild fails?

## A
Returning an error takes search fully down even though a perfectly usable (if slightly stale) index snapshot already exists in memory; scanning the database directly for every search request replaces a fast in-memory lookup with an unprotected full scan of millions of rows, which can overload the database and cascade into failures in the business-write path and the index-builder itself. Falling back to the previous snapshot keeps search serving at full speed with only minutes of staleness, because double buffering means the old snapshot is never discarded until a new one has been fully validated and atomically swapped in — a failed rebuild simply means the swap doesn't happen, not that service is lost.

## Q zh
在一个内存空间索引周期性重建、用双缓冲（double buffering）方式原子切换的邻近搜索系统中，为什么'重建失败时回退到上一份成功加载的索引快照'比'直接返回错误'或'直接扫描商户数据库'这两种降级策略更好？

## A zh
直接返回错误会让搜索完全不可用，即便内存里已经有一份完全可用（只是稍微陈旧）的索引快照；对每个搜索请求都直接扫描数据库，则是把一次快速的内存查找换成了对几百万行数据毫无保护的全表扫描，可能压垮数据库并连带拖垮商户写入路径和索引构建器本身。回退到上一份快照能让搜索继续以全速提供服务，只是数据陈旧几分钟，因为双缓冲机制意味着旧快照在新快照完全验证并原子切换之前永远不会被丢弃——重建失败只意味着这次切换没有发生，不意味着服务丢失。
