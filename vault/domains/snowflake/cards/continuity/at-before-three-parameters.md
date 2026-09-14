---
id: at-before-three-parameters
node: continuity.at-before-statement-syntax
type: cloze
source: snowflake-docs
---
Snowflake 时间旅行（Time Travel）的 `AT | BEFORE` 子句用三种参数定位历史时间点：{{c1::`TIMESTAMP`}}（具体时间戳）、{{c2::`OFFSET`}}（距当前时刻的秒数差，如 `-60*5` 表示 5 分钟前）、{{c3::`STATEMENT`}}（某条已完成语句的查询 ID）。
