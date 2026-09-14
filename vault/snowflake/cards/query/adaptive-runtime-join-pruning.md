---
id: adaptive-runtime-join-pruning
node: query.adaptive-runtime-optimizations
type: qa
tags: [grown]
---
## Q
事实表连接一张经过过滤、只剩少数键的维表时，Snowflake 如何在执行过程中跳过事实表中的整批文件，而这是编译期剪枝做不到的？

## A
在哈希连接中，Snowflake 在处理 build 端（维表侧）记录时收集连接键的分布统计，把这些信息推送到 probe 端（事实表侧），用来过滤行，并在可能时依据微分区（micro-partition）元数据跳过整个文件。编译期无法做到，是因为维表过滤后剩下哪些键要到执行时才知道；这种运行时剪枝也解释了为什么实际扫描的分区数可能少于执行前计划给出的分区数。
