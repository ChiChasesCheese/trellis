---
id: hi-c-sd-camelcamelcamel-n12-timescaledb
node: sd.problem-breakdowns.camelcamelcamel.notes
type: qa
step: 12
---
## Q
**价格追踪服务 · 图表查询：TimescaleDB**｜摘要 · 必会

用 TimescaleDB 怎样替代预聚合批处理？为什么选它而不是 ClickHouse？

## A
- **是什么：** PostgreSQL 的时序扩展，自动按时间分区、压缩，并提供 `time_bucket` 这类时序函数。
- **做法：** 不再跑批，用户请求 6 个月图表时直接查 `SELECT time_bucket('1 day', timestamp), avg(price) FROM prices WHERE product_id = ? GROUP BY 1`，即使数十亿行也能毫秒返回；任意时间范围和粒度都能现算。
- **好处：** 数据实时、无需维护预聚合任务，也不需要第二套数据库，用户、商品、订阅和价格都在同一个 PostgreSQL 生态里，运维简单。
- **为何不是 ClickHouse：** 它的分析性能可能更高，但需要多运维一套系统；这里的查询是按单个商品的时间范围聚合，TimescaleDB 已足够，选运维简单的组合。
- **取舍：** 实时性与简单性换来对扩展的依赖；若分析需求变成全站跨商品的大扫描，再考虑列存。
