---
id: spill-where-to-see-metrics
node: query.spilling-to-remote-disk
type: qa
source: snowflake-docs
---
## Q
怀疑一条 Snowflake 查询发生了溢出（spilling），在查询画像（Query Profile）里应看哪些指标来确认，并区分溢出到了哪一级？

## A
看 Statistics 窗格中的 Spilling 部分：`Bytes spilled to local storage`（溢出到本地磁盘的数据量）和 `Bytes spilled to remote storage`（溢出到远程磁盘的数据量）。再结合 Profile Overview 的耗时分解：`Local Disk IO` 表示处理因访问本地磁盘而阻塞的时间，`Remote Disk IO` 表示因访问远程磁盘而阻塞的时间。远程溢出字节数非零、Remote Disk IO 占比高，说明查询已经掉到了最慢的一级。
