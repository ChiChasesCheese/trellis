---
id: hi-c-sd-key-technologies-n04-nosql
node: sd.in-a-hurry.key-technologies.notes
type: qa
step: 4
---
## Q
**关键技术 · NoSQL 数据库要懂的四样**｜摘要 · 必会

NoSQL 适合什么场景？面试里要讲清它的哪几个特性，有哪些代表产品？

## A
- **适合：** 数据模型还在变、不想先定死 schema；需要横向扩展（加机器而不是换更大的机器）来承载海量数据或高并发；处理大量非结构化或半结构化数据。注意这些都不是关系库的"做不到"，只是 NoSQL 更顺手。
- **数据模型有四种：** 键值（key-value）、文档（document）、列族（column-family）、图（graph）。说产品时要说清它属于哪种。
- **一致性模型：** 从强一致（所有节点同一时刻看到同样的数据）到最终一致（暂时不同，最终收敛）可选；更宽松的一致性换来更高的可用性和延迟表现。
- **索引与扩展：** 和关系库一样支持 B 树、哈希索引；靠一致性哈希（consistent hashing）和分片（sharding）把数据分到很多服务器。
- **代表产品：** DynamoDB（功能广、被广泛接受）、Cassandra（追加式存储，写多场景强，功能上有取舍）、MongoDB。
