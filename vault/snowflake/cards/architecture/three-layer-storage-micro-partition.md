---
id: three-layer-storage-micro-partition
node: architecture.three-layer-model
type: qa
source: snowflake-docs
---
## Q
数据被加载进 Snowflake 表之后，存储层对原始数据做了什么处理？

## A
Snowflake 会把数据重新组织为内部优化过的压缩列式（columnar）格式，并自动切分成许多连续的存储单元，称为微分区（micro-partition）；这些优化后的数据存放在云存储中。Snowflake 全权管理这些数据的组织方式、文件大小、结构、压缩、元数据与统计信息，用户不需要手工管理文件布局。
