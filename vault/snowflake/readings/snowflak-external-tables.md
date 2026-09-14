---
nodes:
- ingestion.external-tables-over-lake
title: 外部表(External Table):原地查询数据湖
corpus: snowflake-docs
section: 36-tables-external-intro
url: https://docs.snowflake.com/en/user-guide/tables-external-intro
tags:
- canonical
---

# 外部表(External Table):原地查询数据湖

外部表让 Snowflake 像查询自己的表一样查询存放在外部 stage(客户云存储桶)里的文件,数据的唯一真源仍留在外部存储,Snowflake 不复制、不管理这些字节。默认只有一个 VARIANT 类型的 VALUE 列承载整行原始内容,若熟悉源文件结构,可以在此基础上定义虚拟列做强类型校验。为提升查询性能,推荐按日期、地区等维度对底层文件做路径分区(partition),外部表可以据此按路径表达式自动发现分区,也可以手工维护分区元数据。因为查询外部表通常比原生表慢,常见做法是在其上建物化视图,或干脆迁移到 Apache Iceberg 表以获得更好的查询语义和性能。
