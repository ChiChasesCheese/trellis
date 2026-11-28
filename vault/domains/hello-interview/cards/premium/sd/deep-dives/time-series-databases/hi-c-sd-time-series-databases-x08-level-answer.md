---
id: hi-c-sd-time-series-databases-x08-level-answer
node: sd.deep-dives.time-series-databases.exam
type: qa
step: 8
---
## Q
**时序数据库 · 中级与资深答案的差别**｜考点 · 必会

面试官说「设计监控系统的存储」。中级会怎么答？资深在此之上多说什么？

## A
- **中级：** 「用 InfluxDB 或 Prometheus 这类时序库」，会说一点追加写和压缩，答出能存就行。
- **资深追加的内容：**
  - 先算数：5 万点/秒、一天 43 亿点，说明为什么 Postgres 不够。
  - 讲清取舍：LSM 写快读慢，用布隆过滤器和分区补读。
  - 谈判需求：主动提降采样，一周细粒度，之后 5 分钟、1 小时。
  - 点出风险：标签基数，哪些值只能当字段。
  - 说明边界：Top-K 之类跨序列聚合不适合，必要时换别的存储。
