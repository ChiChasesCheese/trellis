---
id: stages-put-vs-cloud-upload
node: ingestion.file-formats-and-stages
type: qa
source: snowflake-docs
---
## Q
把本地文件放进内部暂存区和放进外部暂存区，分别用什么工具？外部暂存区可以指向与 Snowflake 账户不同云平台的存储吗？

## A
内部暂存区（用户、表、命名）用 Snowflake 的 `PUT` 命令从本地文件系统上传。外部暂存区的文件要用云存储服务自己提供的工具上传。无论 Snowflake 账户托管在哪个云平台，都可以从 Amazon S3、Google Cloud Storage、Microsoft Azure 加载；但如果云存储位于不同区域或不同云平台，可能产生数据传输费用。
