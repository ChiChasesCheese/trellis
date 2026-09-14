---
id: copy-into-simple-transformations
node: ingestion.bulk-copy-into
type: cloze
source: snowflake-docs
---
`COPY INTO <table>` 在加载过程中支持的简单转换：{{c1::列重新排序}}、{{c2::省略部分列}}、{{c3::类型转换（cast）}}、{{c4::截断超出目标列长度的文本}}。因此数据文件的列数和列顺序{{c5::不必}}与目标表一致。
