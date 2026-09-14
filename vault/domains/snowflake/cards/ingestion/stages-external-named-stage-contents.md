---
id: stages-external-named-stage-contents
node: ingestion.file-formats-and-stages
type: qa
source: snowflake-docs
---
## Q
命名外部暂存区（named external stage）这个对象里保存了什么？为什么把文件格式选项放在暂存区上能简化 COPY INTO？

## A
命名外部暂存区是模式中的数据库对象，保存云存储中文件的 URL、访问该云存储账户所需的设置，以及描述暂存文件格式的选项等便利设置。把文件格式（如分隔符、压缩方式、JSON/Parquet 类型）定义在暂存区或具名文件格式对象上，COPY INTO 只需引用暂存区，不必每条语句都重复写解析参数，多个加载作业也能保持一致。
