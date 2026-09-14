---
id: unload-copy-into-location-basics
node: ingestion.unload-export
type: qa
tags: [grown]
---
## Q
把 Snowflake 中的查询结果导出为文件交给下游系统，用什么命令？它与加载时的 `COPY INTO <table>` 是什么关系？

## A
用 `COPY INTO <location>`，目标可以是内部暂存区、外部暂存区或直接写云存储 URL，来源可以是一张表，也可以是任意 SELECT 查询。它是加载的反方向：`COPY INTO <table>` 把暂存文件读入表，`COPY INTO <location>` 把表或查询结果写成暂存区中的文件，同样可以指定文件格式（CSV、JSON、Parquet）和压缩方式；导出到内部暂存区后，可再用 `GET` 下载到本地。
