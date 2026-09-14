---
id: stream-stores-only-offset
node: pipelines.stream-offset-bookmark
type: qa
source: snowflake-docs
---
## Q
Snowflake 的流（Stream，变更数据捕获对象）里存的是源表变更数据的副本吗？查询它时，变更记录是从哪里来的？

## A
不是。流本身不包含任何表数据，只保存一个偏移量（offset），即源对象某个事务版本之间的时间点，就像夹在书里的书签。查询流时，Snowflake 结合流中存储的偏移量和源表中的变更追踪元数据，利用源对象的版本历史计算出自该偏移量以来的变更。创建第一个流时，源表会被加上几个隐藏列来存放变更追踪元数据，只占少量存储。
