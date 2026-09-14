---
id: analytics-star-schema
node: analytics.olap
type: qa
---
## Q
Describe the star schema, and why warehouses tolerate wide, denormalized dimension tables that would be bad OLTP design.

## A
One huge **fact table** of events (sale, click, shipment) — each row a narrow record of foreign keys plus numeric measures — surrounded by **dimension tables** (who/what/where/when: product, customer, date) that give the keys meaning.

Facts are append-only and billions of rows; dimensions are small (thousands–millions) and change rarely. Denormalizing dimensions (flattening the "snowflake") is fine because update anomalies barely matter for slowly-changing reference data, while fewer joins means simpler, faster queries.

Analysts' queries then follow one shape: filter/group by dimension attributes, aggregate fact measures.

## Q zh
描述 star schema，为什么 warehouse 容忍宽、去规范化维度表，这对 OLTP 设计会很坏。

## A zh
一个巨大**事实表**的事件（sale、click、shipment）— 每行一条外键加数值度量的狭隘记录 — 被**维度表**（who/what/where/when：product、customer、date）包围，给 key 意义。

事实是追加只的和数十亿行；维度是小的（数千–数百万）和很少改变。去规范化维度（平坦化"雪花"）很好，因为更新异常对慢变化参考数据几乎无关，而较少 join 意味着更简单、更快的查询。

分析师的查询然后遵循一个形状：按维度属性过滤/group、聚合事实度量。
