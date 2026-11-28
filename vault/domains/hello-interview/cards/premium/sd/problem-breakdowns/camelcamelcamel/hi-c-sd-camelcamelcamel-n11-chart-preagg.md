---
id: hi-c-sd-camelcamelcamel-n11-chart-preagg
node: sd.problem-breakdowns.camelcamelcamel.notes
type: qa
step: 11
---
## Q
**价格追踪服务 · 图表查询：为什么慢，预聚合怎么做**｜摘要 · 必会

价格历史图表要在 500ms 内返回，为什么直接查 PostgreSQL 会慢？每晚预聚合的方案怎么做？

## A
- **为什么慢：** 起步是一张 PostgreSQL 价格表，索引 `(product_id, timestamp)`。热门商品几年里每几小时一个点，累积成数千行；两年图表要把它们聚合成日或周的桶，原始查询在这个聚合上吃力。
- **预聚合：** 每晚跑批处理，对前一天的数据算出每个时间段的平均、最低、最高、开盘、收盘价，存进一张 `price_aggregations` 表，用 `granularity` 列区分日、周、月。
- **查询：** 30 天图用日聚合，两年图用月聚合；索引 `(product_id, granularity, date)`，只读几十行，毫秒返回。
- **代价：** 图表最多滞后 24 小时（对看历史趋势基本可接受）；要额外存储，但随商品数和粒度线性增长。
- **何时选它：** 数据库已经是 PostgreSQL、不想引入新组件，且能接受隔夜的新鲜度。
