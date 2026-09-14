---
id: qas-outlier-offload-mechanism
node: pruning.query-acceleration-service
type: qa
source: snowflake-docs
---
## Q
一个虚拟仓库（warehouse）平时负载正常，但偶尔有几条扫描量巨大的离群查询（outlier query）拖慢整体。查询加速服务（Query Acceleration Service, QAS）是怎样缓解这个问题的？它加速哪两类查询？

## A
QAS 把这类查询中可并行的部分（主要是扫描和过滤）卸载（offload）到服务提供的共享计算资源上，用超出仓库自身规模的并行度来缩短扫描/过滤的墙钟时间，从而降低离群查询对整个仓库的冲击。它加速两类模式：(1) 大扫描加选择性过滤或聚合的查询；(2) 插入、复制、更新或删除大量数据的语句（如 INSERT、COPY）。由于依赖共享资源的可用性，加速效果会随时间波动。
