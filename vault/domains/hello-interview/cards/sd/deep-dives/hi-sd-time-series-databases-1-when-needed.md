---
id: hi-sd-time-series-databases-1-when-needed
node: qb.sd.top-k-counts.pre-sd-deep-dives-time-series-databases
type: qa
step: 1
---
## Q
**什么时候才需要时序数据库**｜系统设计 · 深入专题

有时间戳的数据就该用时序数据库（TSDB）吗？以监控 10 万台服务器为例，用普通 Postgres 存会出什么问题，面试里应该怎么决策？

## A
**数字。** 10 万台服务器，每台每 10 秒上报 5 个指标：每秒 5 万个数据点，一天约 43 亿个，一周约 300 亿行。用 Postgres 的 `(timestamp, host, metric_name, value)` 宽表，会遇到：
- 单机扛不住每秒 5 万次写入（突发更高），索引越多写越慢
- **简单查询也很慢：** 简单查询（某主机过去一小时的平均 CPU）也很慢
- 存储浪费：每行重复存主机名和指标名，50 到 100 字节，而有效信息只有时间戳加浮点数共 16 字节

InfluxDB、TimescaleDB、Prometheus 就是为这种负载造的。

**易错。** 有时间序列数据不等于需要时序数据库。例如 Top-K（热门榜）：要在海量序列之间排序聚合，这正是多数时序库不擅长的，用了反而更难。

**取舍。** 先尽量用 Postgres、DynamoDB 这类通用数据库撑住，真遇到无法用别的办法解决的瓶颈，才上专用技术。理解它的限制，才知道何时适用。
