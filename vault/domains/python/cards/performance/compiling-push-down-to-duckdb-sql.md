---
id: compiling-push-down-to-duckdb-sql
node: performance.compiling
type: qa
tags: [grown]
---
## Q
为什么「把过滤、分组、连接这类操作用 SQL 交给 DuckDB 这样的查询引擎去做」，往往比「自己写 Python 循环再手动调优」更划算？

## A
查询引擎已经把聚合、过滤、join 这类关系代数操作用向量化执行、多线程、以及基于统计信息的查询优化器实现得很成熟；用几行 SQL 描述「要什么」，引擎自己决定「怎么算最快」，往往比自己一行行调优 Python 循环省时间也跑得更快——除非计算本身不是关系代数操作（比如自定义的迭代算法），这时查询引擎帮不上忙。
