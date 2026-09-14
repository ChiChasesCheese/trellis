---
id: qas-ineligible-reasons
node: pruning.query-acceleration-service
type: qa
source: snowflake-docs
---
## Q
开启了查询加速服务（QAS）后，某条查询依然没有被加速。常见的不符合条件（ineligible）的原因有哪些？为什么“扫描的分区太少”反而不能加速？

## A
常见原因：(1) 扫描的微分区数量不够多——此时申请 QAS 资源的延迟会抵消并行带来的收益；(2) 过滤条件选择性不够，或 GROUP BY 表达式的基数（cardinality）太高；(3) 含有阻止加速的 LIMIT 子句；(4) 使用了返回非确定性结果的函数（如 `SEQ`、`RANDOM`）。Snowflake 没有固定的“足够大”阈值，只在高度确信能加速时才把查询标为符合条件。
