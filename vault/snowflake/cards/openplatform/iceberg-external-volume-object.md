---
id: iceberg-external-volume-object
node: openplatform.iceberg-tables
type: qa
source: snowflake-docs
---
## Q
Snowflake 中的外部卷（external volume）是什么对象？它解决什么问题，有哪些配置约束？

## A
外部卷是账户级的具名 Snowflake 对象，保存一个指向客户存储位置的 IAM（身份与访问管理）实体，Snowflake 用它安全地访问表数据文件、Iceberg 元数据以及记录模式和分区的清单文件（manifest）。一个外部卷可以支撑多张 Iceberg 表。约束：外部卷的存储位置不能通过 storage integration 访问；每个外部卷都要单独配置信任关系；Snowflake 不支持名称中含点号的 S3 桶，因为它使用虚拟主机风格路径加 HTTPS，而 S3 对这类桶不支持 SSL。
