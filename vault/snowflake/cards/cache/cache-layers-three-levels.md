---
id: cache-layers-three-levels
node: cache.cache-layer-tradeoffs
type: cloze
tags: [grown]
---
Snowflake 查询路径上的三层缓存，由浅到深：
1. {{c1::结果缓存（result cache）}}——存放在云服务层，命中时连仓库都不需要；
2. {{c2::元数据缓存（metadata cache）}}——微分区的行数与 min/max 等统计，用于剪枝和简单聚合；
3. {{c3::仓库本地磁盘缓存（warehouse local disk cache）}}——仓库节点 SSD 上缓存的原始微分区数据，挂起即丢失。
