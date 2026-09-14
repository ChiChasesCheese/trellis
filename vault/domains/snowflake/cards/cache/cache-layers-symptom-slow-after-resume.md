---
id: cache-layers-symptom-slow-after-resume
node: cache.cache-layer-tradeoffs
type: qa
tags: [grown]
---
## Q
一条每天早上跑的报表查询，SQL 和数据都与昨天相同，但今天仍花了几分钟、并且查询剖析（Query Profile）显示从远程存储读取的比例很高。应该怀疑哪一层缓存没有生效？

## A
「读远程存储比例高」说明仓库本地磁盘缓存（warehouse local disk cache，节点 SSD 上的数据缓存）是冷的，典型原因是仓库夜间自动挂起（auto-suspend）后缓存被清空。同时结果缓存（result cache，直接复用上次结果）显然也没命中——如果命中就不会扫描任何数据，常见原因是查询中含 `CURRENT_TIMESTAMP()` 之类每次结果不同的函数，或底层表在夜间有过写入。
