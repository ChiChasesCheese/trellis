---
id: hi-c-sd-scaling-writes-x08-cassandra-vs-pg
node: sd.patterns.scaling-writes.exam
type: qa
step: 8
---
## Q
**写扩展 · 为什么写密集选 Cassandra**｜考点 · 必会

日志采集每秒几十万写入、读很少，选 PostgreSQL 还是 Cassandra？怎么解释？

## A
- **倾向 Cassandra / 时序库：** 追加式提交日志，顺序写盘，避免原地更新的磁盘寻道；同样硬件下写吞吐通常明显高于传统关系库，倍数取决于数据模型与负载。
- **代价：** 读性能一般，要检查多个文件并合并，也没有关系库的事务与灵活查询。
- **取舍说明：** 优化写常损害读，要先确认瓶颈在写还是读；这个场景读很少，正好符合。
- **指标类数据：** 更适合时序库（InfluxDB、TimescaleDB），分析型用列存（ClickHouse）。
- **前提：** 写入量大到值得围绕它设计架构，否则 PostgreSQL 配合调优就够了。
