---
id: kafka-internals-open-file-handles
node: internals.storage-segments
type: qa
step: 6
source: kafka-2e
---
## Q
一个 Kafka broker 往往要为分区维护许多个日志片段（log segment）文件，这会给操作系统层面带来什么运维上的注意点？

## A
broker 会为分区的每一个已打开的日志片段分配一个文件句柄（file handle），哪怕这个片段已经不是当前正在写入的活动片段、只是保留期内的历史数据。当一个 broker 上分区和片段数量都很多时，同时打开的文件句柄数会相当可观，因此需要针对操作系统的文件句柄上限等参数做相应调优，否则可能因句柄耗尽而出问题。
