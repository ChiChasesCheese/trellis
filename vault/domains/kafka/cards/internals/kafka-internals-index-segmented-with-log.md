---
id: kafka-internals-index-segmented-with-log
node: internals.indexes
type: qa
source: kafka-2e
---
## Q
Kafka 的日志片段（log segment）会随着数据被删除而整体清理掉；那配套的偏移量索引和时间索引要怎么处理，才不会留下指向已删除数据的悬空条目？

## A
索引本身也和日志一样被切分成对应的片段：每个日志片段都有自己配套的一段索引文件。当某个日志片段因为超出保留期限被删除时，与它对应的那部分索引也一起被删除，两者是绑定在一起管理的，因此不会出现索引残留、指向已经不存在的日志片段的情况。
