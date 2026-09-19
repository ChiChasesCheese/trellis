---
id: kafka-connect-converter-decouples-format
node: connect.connect-basics
type: qa
step: 5
source: kafka-2e
---
## Q
Connect 的「转换器（converter）」在整个数据流转过程中扮演什么角色？它是怎么让「连接器要接入什么系统」和「数据在 Kafka 里以什么格式存储」这两件事互不影响、可以自由组合的？

## A
数据源连接器（比如 JDBC 连接器）读取外部系统的数据后，会用 Connect 自带的一套内存对象模型（Schema 描述字段类型，Struct 保存具体字段值）来表示这条记录，而不是直接生成 JSON、Avro 这类具体格式；真正把这个内存对象序列化成 Kafka 里存储的字节格式（比如 JSON、Avro、Protobuf、纯字符串等）的工作，是由 worker 按配置调用相应的**转换器**来完成的，反方向（从 Kafka 读出字节、还原成 Schema+Struct 交给数据池连接器）同理。因为连接器只关心「怎么从外部系统读/写数据」，转换器只关心「Connect 内存对象和 Kafka 存储字节之间怎么互转」，两者互不耦合，用户可以给任意连接器搭配任意一种可用的转换器。
