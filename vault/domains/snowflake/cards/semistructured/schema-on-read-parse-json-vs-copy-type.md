---
id: schema-on-read-parse-json-vs-copy-type
node: semistructured.schema-on-read-parsing
type: qa
source: snowflake-docs
---
## Q
要把 JSON 数据变成可查询的 VARIANT 值，「在 COPY INTO 中指定 `TYPE = JSON`」和「调用 `PARSE_JSON`」这两种方式有什么区别？

## A
两种方式都是把输入格式和目标 Snowflake 类型对上。COPY INTO 方式在建表时声明 VARIANT 列，在 `COPY INTO <table>` 的文件格式中用 `TYPE = JSON` 声明输入格式，适合批量加载暂存区（stage）中的文件。`PARSE_JSON` 是函数，把一个 JSON 字符串转换为 VARIANT 值，适合在 INSERT … SELECT 或查询中处理已经以文本形式存在的 JSON。
