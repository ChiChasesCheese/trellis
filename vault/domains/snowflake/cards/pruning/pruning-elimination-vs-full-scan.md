---
id: pruning-elimination-vs-full-scan
node: pruning.partition-elimination
type: qa
source: snowflake-docs
---
## Q
分区消除（partition elimination）把一次原本的全表扫描变成了什么？这个转变发生在查询处理的哪个环节？

## A
它把“扫描全表所有微分区（micro-partition）”转变成“只扫描通过剪枝判断后存活下来的那一小部分微分区”。这个转变发生在查询编译阶段：优化器根据谓词和每个微分区的元数据，在生成执行计划时就已经确定了哪些微分区需要参与执行，不需要等到运行时再逐个探测。
