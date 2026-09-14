---
id: auto-recluster-classic-vs-optima
node: storage.automatic-reclustering
type: qa
source: snowflake-docs
---
## Q
自动聚簇（Automatic Clustering）的 Clustering Classic 与 Optima Clustering 在计费和适用表上有什么区别？已经在 Classic 上的表能迁到 Optima 吗？

## A
Classic 按无服务器（serverless）计算小时计费，表变动越多维护成本越高，另可能因重写数据增加 Fail-safe（故障保护）存储；Optima 按摄入数据量乘重叠因子计费，费用更可预测，聚簇新数据更快，并且键长度可用到所有列合计 1 KB（Classic 每列只取前 5 字节）。从 2026-09-01 起新定义聚簇的表使用 Optima，已聚簇的表会无限期留在 Classic：用 ALTER TABLE 修改聚簇键不会迁移，也没有迁移命令。
