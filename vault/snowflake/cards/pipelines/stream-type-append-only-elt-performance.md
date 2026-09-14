---
id: stream-type-append-only-elt-performance
node: pipelines.stream-types
type: qa
source: snowflake-docs
---
## Q
一个 ELT 管道的暂存表只接收 INSERT，每次消费完流之后立即 TRUNCATE 暂存表。为什么这里选仅追加流（append-only stream）比标准流更合适？

## A
仅追加流只返回追加进来的行，不需要像标准流那样对插入和删除做连接来计算净变化，因此性能明显更好。而且消费完立即 TRUNCATE 源表所产生的删除记录，不会增加下一次查询或消费流时的开销；若用标准流，这些删除都要参与计算。
