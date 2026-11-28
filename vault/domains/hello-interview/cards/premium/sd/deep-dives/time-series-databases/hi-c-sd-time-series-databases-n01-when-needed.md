---
id: hi-c-sd-time-series-databases-n01-when-needed
node: sd.deep-dives.time-series-databases.notes
type: qa
step: 1
---
## Q
**时序数据库 · 为什么普通 Postgres 撑不住**｜摘要 · 必会

监控系统每天写入几十亿个数据点，为什么单机 Postgres 不行？什么时候才值得上时序数据库（TSDB）？

## A
- **场景数字：** 10 万台服务器，每台每 10 秒上报 5 个指标，写入约 5 万点/秒，一天约 43 亿点，一周约 300 亿行。
- **三个痛点：** 一是写入：多建索引会拖慢写入，5 万次/秒的持续写加突发会压垮单实例；二是查询：「某主机过去一小时的平均 CPU」要在百亿行里找；三是存储：每行重复存主机名和指标名，一个点 50–100 字节，而真正的信息只有时间戳加浮点数，约 16 字节。
- **TSDB 是什么：** InfluxDB、TimescaleDB、Prometheus 这类库，专门针对「只追加、按时间查」的负载设计。
- **别过早上：** 有时间戳不等于要用 TSDB。能先用 Postgres 或 DynamoDB 撑住就先撑，遇到真正的瓶颈再换专用库；例如 Top-K 要跨海量序列排序聚合，TSDB 反而不擅长。
