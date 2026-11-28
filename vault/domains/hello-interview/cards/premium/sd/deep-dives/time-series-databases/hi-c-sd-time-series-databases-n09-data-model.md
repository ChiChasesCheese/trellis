---
id: hi-c-sd-time-series-databases-n09-data-model
node: sd.deep-dives.time-series-databases.notes
type: qa
step: 8
---
## Q
**时序数据库 · 数据模型：指标、标签、字段**｜摘要 · 必会

时序库里的一个数据点由哪几部分组成？标签（tag）和字段（field）有什么区别，选错会怎样？

## A
- **四个部分：** 指标名（measurement，类似表名，如 `cpu_usage`）；标签（tags，带索引的元数据，如 `host`、`region`）；字段（fields，真正测量的值，如 `value=45.2`）；时间戳。
- **一个点：** `cpu_usage,host=s1,region=us value=45.2 <ts>`。
- **索引差异：** 标签被索引，按标签过滤很快；字段不索引，是被存储的时间序列本身。
- **怎么选：** 要拿来过滤、分组的（主机、区域、服务）放标签；要度量的数值放字段。
- **选错的后果：** 把度量值放标签，查询性能差，还会触发基数爆炸；把过滤维度放字段，则无法快速过滤。
