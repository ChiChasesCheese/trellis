---
id: explain-spot-cartesian-join
node: query.explain-plan-interpretation
type: qa
tags: [grown]
---
## Q
一条多表连接查询写完后担心漏了连接条件，怎样在不执行查询的前提下用 EXPLAIN 发现问题？

## A
在 EXPLAIN 输出中查看 operation 列和连接表达式：若出现 CartesianJoin（笛卡尔积连接）算子，或某个 Join 行没有等值连接条件，说明有表之间缺少连接谓词，执行时输出行数会呈乘积式爆炸。同时检查 Filter 是否出现在对应 TableScan 附近、各表的 partitionsAssigned 是否合理，就能在花费任何仓库 credit 之前修正查询。
