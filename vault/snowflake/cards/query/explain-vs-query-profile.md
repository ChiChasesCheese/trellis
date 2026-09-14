---
id: explain-vs-query-profile
node: query.explain-plan-interpretation
type: qa
tags: [grown]
---
## Q
EXPLAIN 执行计划与查询画像（Query Profile）有何区别？为什么两者给出的分区数或算子可能对不上？

## A
EXPLAIN 是运行前的计划，展示编译期决定要做的操作及其关系，数字来自编译期（如剪枝后分配的分区数）；查询画像是运行后的实际执行记录，包含真实扫描的分区数、耗时、溢出等统计。二者可能不同，因为部分决策和优化在执行时才发生，例如运行时依据连接另一侧的数据进一步跳过分区。所以 EXPLAIN 的 partitionsAssigned 应视为上界，确认真实效果要看执行后的画像。
