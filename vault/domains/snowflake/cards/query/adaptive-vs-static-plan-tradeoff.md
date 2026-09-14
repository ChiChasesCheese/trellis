---
id: adaptive-vs-static-plan-tradeoff
node: query.adaptive-runtime-optimizations
type: qa
tags: [grown]
---
## Q
与完全依赖编译期估算的静态计划相比，运行时自适应优化在“可预测性”上带来什么影响？排查性能时应注意什么？

## A
自适应优化让同一条 SQL 在数据分布变化时自动调整执行方式，平均表现更稳，但也意味着执行前看到的计划不一定就是实际执行的样子，同一查询在不同数据量下可能走不同的连接分布或跳过不同数量的分区。排查性能时应以执行后的查询画像（Query Profile）中的实际统计（真实扫描分区数、各算子输入输出行数、耗时）为准，而不是只看执行前的计划。
