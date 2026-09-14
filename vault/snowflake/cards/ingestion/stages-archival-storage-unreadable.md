---
id: stages-archival-storage-unreadable
node: ingestion.file-formats-and-stages
type: qa
source: snowflake-docs
---
## Q
外部暂存区指向的 S3 前缀里，一部分历史文件已被生命周期规则转为 Glacier Deep Archive。COPY INTO 能加载这些文件吗？

## A
不能。Snowflake 无法访问需要先恢复（restore）才能读取的归档存储类别中的数据，例如 Amazon S3 Glacier Flexible Retrieval、Glacier Deep Archive，或 Microsoft Azure Archive Storage。需要先在云存储侧把文件恢复到可直接读取的存储类别，再执行加载。
