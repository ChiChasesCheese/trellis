---
nodes:
- ingestion.bulk-copy-into
- ingestion.file-formats-and-stages
title: 数据加载总览:内部/外部 stage 与批量 COPY INTO
corpus: snowflake-docs
section: 18-data-load-overview
url: https://docs.snowflake.com/en/user-guide/data-load-overview
tags:
- canonical
---

# 数据加载总览:内部/外部 stage 与批量 COPY INTO

Snowflake 用 stage 统一指代云存储中文件的落脚点:外部 stage 是客户自己名下的 S3/GCS/Azure 容器,内部 stage(用户级、表级或具名)则由 Snowflake 托管。批量加载用 COPY INTO 命令,依赖用户自建的虚拟仓库,可以在加载过程中做列重排、列裁剪、类型转换等简单变换,且源文件的列数和顺序不必与目标表完全一致,天然支持跨多个文件的并行加载。与之相对的 Snowpipe 走 serverless 计算、面向小批量持续到达的文件。读完应能判断:面对稳定的大批量文件,选批量 COPY 更省心;面对持续、零散到达的文件,该考虑另一条路径。
