---
nodes:
- openplatform.iceberg-tables
- openplatform.polaris-catalog
- openplatform.external-engine-commit-protocol
title: Apache Iceberg 表:开放格式与目录(Catalog)选型
corpus: snowflake-docs
section: 30-tables-iceberg
url: https://docs.snowflake.com/en/user-guide/tables-iceberg
tags:
- canonical
---

# Apache Iceberg 表:开放格式与目录(Catalog)选型

Iceberg 表把 Snowflake 表的查询语义带到客户自己管理的云对象存储上,数据和元数据文件都以开放的 Parquet + Iceberg 规范存放,天然支持外部引擎读写。目录(catalog)是 Iceberg 规范的第一层架构组件,负责保存“表名指向哪个元数据文件”的当前指针并保证该指针更新的原子性;既可以用 Snowflake 自身作目录(全平台功能完整),也可以通过目录集成(catalog integration)对接外部 REST 目录,例如 AWS Glue 或引擎无关的开源目录 Snowflake Open Catalog(即 Apache Polaris 的落地形态)。当外部引擎向 Snowflake 管理的表写入时,Snowflake 会保证先把变更提交到远端目录、再更新本地表状态,以此保证跨引擎写入的原子性。
