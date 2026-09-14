---
id: explain-compiles-not-executes
node: query.explain-plan-interpretation
type: qa
tags: [grown]
---
## Q
在 Snowflake 中对一条可能跑一小时的查询先执行 `EXPLAIN`，会不会启动或消耗虚拟仓库（virtual warehouse）？它有什么开销？

## A
不会。EXPLAIN 只编译 SQL 语句而不执行它，因此不需要运行中的仓库，也不消耗仓库的计算 credit。唯一的开销是编译本身在云服务（Cloud Services）层消耗的云服务 credit。这使它适合在提交昂贵查询之前低成本地检查执行计划。
