---
id: external-table-silent-skip-errors
node: ingestion.external-tables-over-lake
type: qa
source: snowflake-docs
---
## Q
外部表查询没有报错，但结果行数比源文件少。可能有哪些「静默丢行」的原因？

## A
1) 扫描云存储文件时遇到错误，Snowflake 会跳过该文件继续扫描下一个，甚至只返回该文件出错前已扫描的行；2) 含有无效 UTF-8 数据的记录会从结果中省略且不报错，可以在文件格式中设置 `REPLACE_INVALID_CHARACTERS = TRUE`，用替换字符 `�` 替代无效字符来保留这些记录。排查时可以用 `EXTERNAL_TABLE_FILE_REGISTRATION_HISTORY` 查看刷新元数据时的错误。
