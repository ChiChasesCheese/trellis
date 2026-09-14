---
id: compression-no-user-encoding-ddl
node: storage.columnar-compression-encoding
type: qa
source: snowflake-docs
---
## Q
从其他列式数仓迁移到 Snowflake 时，工程师想为每列手工指定编码（encoding）和压缩方式，这在 Snowflake 中需要做吗？

## A
不需要。数据加载进 Snowflake 表时会被重组为内部优化的压缩列式格式，数据的组织方式、文件大小、结构、压缩、元数据和统计信息都由 Snowflake 全权管理，压缩算法按微分区（micro-partition）逐列自动选择。用户无法也无需逐列调优编码。
