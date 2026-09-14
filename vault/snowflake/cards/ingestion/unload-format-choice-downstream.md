---
id: unload-format-choice-downstream
node: ingestion.unload-export
type: qa
tags: [grown]
---
## Q
导出数据给下游 Spark 分析作业和给业务方用 Excel 打开，应分别选择什么文件格式？为什么？

## A
给 Spark 选 Parquet：列式存储、自带数据类型，读取时可以只读需要的列，压缩率高，也不存在分隔符转义问题。给业务方选 CSV（按需压缩或不压缩）：通用、可以直接打开，但丢失类型信息，需要注意分隔符、引号和 NULL 的表示方式，并用 `HEADER = TRUE` 输出列名。半结构化数据如需保留嵌套结构，可以导出为 JSON。
