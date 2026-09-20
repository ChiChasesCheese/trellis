---
id: kafka-internals-offset-index-purpose
node: internals.indexes
type: qa
step: 1
source: kafka-2e
---
## Q
消费者要求从偏移量（offset，消息在分区里的位置编号）100 开始读 1 MB 消息，而这个偏移量可能落在分区众多日志片段（log segment）文件中的任意一个里。如果没有额外的索引结构，broker 要怎么找到它，为什么这样做不可取？

## A
没有索引的话，broker 只能从某个片段的文件开头开始顺序扫描，逐条读取消息、累加它们占的字节数，直到找到目标偏移量对应的那条消息——分区数据量越大，这种线性扫描越慢。为此 Kafka 为每个分区维护一个**偏移量索引**，直接记录「某个偏移量」到「它在哪个片段文件、文件内哪个字节位置」的映射，使 broker 能一步跳到目标位置附近，不必扫描整个日志。
