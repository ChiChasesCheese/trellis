---
id: kafka-internals-index-corruption-recovery
node: internals.indexes
type: qa
step: 4
source: kafka-2e
---
## Q
偏移量索引或时间索引文件如果损坏了，或者管理员手动把它删除了，Kafka 会丢失定位消息的能力吗？为什么说手动删除索引「绝对安全」？

## A
不会永久丢失。Kafka 并不为索引文件维护校验和（checksum），一旦发现索引损坏，它会重新扫描一遍对应的日志片段，边读消息边记录每条消息的偏移量和文件位置，从而重新生成索引；管理员即便主动删除索引文件也是安全的，因为 Kafka 会自动检测到索引缺失并重建，唯一的代价是重建过程需要重新扫描日志，如果数据量很大，恢复所需的时间会比较长。
