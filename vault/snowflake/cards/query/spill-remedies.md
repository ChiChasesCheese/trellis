---
id: spill-remedies
node: query.spilling-to-remote-disk
type: qa
source: snowflake-docs
---
## Q
一条查询在查询画像（Query Profile）中显示大量字节溢出（spilling）到远程存储，有哪两种缓解手段？各自为什么有效？

## A
① 换用更大的虚拟仓库（virtual warehouse）：更大的规格意味着每个集群有更多计算资源，相当于给该操作增加了可用内存和本地磁盘空间，中间结果能留在内存或本地盘，不再落到远程磁盘。② 把数据分成更小的批次处理：每批的中间结果变小，能装进现有内存。前者用更高的每小时 credit（信用点）换速度，后者用改写作业换资源。
