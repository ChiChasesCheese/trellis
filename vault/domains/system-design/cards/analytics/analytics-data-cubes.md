---
id: analytics-data-cubes
node: analytics.olap
type: qa
---
## Q
A dashboard slices sales by any combination of date, product, store, and promotion, and every query answers in milliseconds without scanning the fact table. What structure makes that possible, and what does it fundamentally give up?

## A
A **data cube (OLAP cube)**: a materialized grid of aggregates precomputed along the dimensions — e.g. `SUM(net_price)` for every (date, product) cell, plus subtotal rollups along each edge and the grand total. A query like "revenue for store 42 in March" reads or sums a handful of precomputed cells instead of scanning raw facts; drill-down and roll-up walk the same structure.

What it gives up: **flexibility to ask anything not baked in**.
- Only the chosen dimensions and measures exist — "for customers over 30" is unanswerable if age isn't a dimension.
- Only aggregates that combine hierarchically work well (SUM/COUNT/MIN/MAX compose from sub-cells; COUNT DISTINCT and medians don't, without sketches).
- Adding a dimension multiplies cells and maintenance cost; updates to history mean recomputing affected cells.

Practice: keep the raw fact table (columnar) as the source of truth for arbitrary questions, and lay cubes/summary tables on top as a **performance optimization for the known, hot query shapes** — a materialized view, recomputable at will.

## Q zh
一个仪表盘可以按日期、商品、门店、促销的任意组合切分销售数据，每个查询都在毫秒级返回，而且从不扫描事实表。什么结构使之成为可能？它从根本上放弃了什么？

## A zh
**数据立方体（data cube / OLAP cube）**：沿各维度预先计算好的聚合网格——例如每个（日期，商品）单元格里存 `SUM(net_price)`，再加上每条边上的小计 rollup 和总计。"42 号门店三月的营收"这类查询只需读取或累加少数几个预计算单元格，而不是扫描原始事实；下钻（drill-down）和上卷（roll-up）走的是同一套结构。

它放弃的是：**问任何没有预先烘焙进去的问题的自由**。
- 只有选定的维度和度量存在——如果年龄不是一个维度，"30 岁以上的客户"就无法回答。
- 只有能按层级组合的聚合才好用（SUM/COUNT/MIN/MAX 可以由子单元格合成；COUNT DISTINCT 和中位数不行，除非用 sketch）。
- 每加一个维度，单元格数量和维护成本成倍增长；修改历史数据意味着重算受影响的单元格。

实践：保留原始（列式）事实表作为任意问题的事实源，把 cube/汇总表铺在上面，当作**面向已知热点查询形态的性能优化**——本质是一个可随时重算的物化视图。
