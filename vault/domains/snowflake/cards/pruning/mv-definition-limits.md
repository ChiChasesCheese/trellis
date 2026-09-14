---
id: mv-definition-limits
node: pruning.materialized-views-maintenance
type: cloze
source: snowflake-docs
---
Snowflake 物化视图（materialized view）的定义限制：只能查询{{c1::单张表}}，不支持{{c2::JOIN（包括自连接）}}；不能包含{{c3::UDF、窗口函数、HAVING、ORDER BY、LIMIT、嵌套子查询}}；所有 GROUP BY 键必须{{c4::出现在 SELECT 列表中}}。
