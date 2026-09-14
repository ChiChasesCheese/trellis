---
id: storage-compute-separation
node: storage.object
type: qa
---
## Q
Storage–compute separation (Snowflake, BigQuery, modern lakehouses): what does putting the data in object storage buy, and what latency problem does it create?

## A
Buys **independent scaling and elasticity**: spin compute to zero or burst to hundreds of nodes without moving data; multiple engines (SQL, Spark, ML) read the same files; storage is cheap, durable, and effectively infinite.

Creates a latency problem: object-store reads are **tens of ms first-byte over the network** vs local NVMe µs — so every serious engine adds **local SSD/memory caching of hot data** and columnar formats + metadata pruning to read as few bytes as possible. It fits analytics; OLTP still wants storage next to compute.

## Q zh
存储-计算分离（Snowflake、BigQuery、现代数据湖）：把数据放在对象存储中有什么好处，它创造了什么延迟问题？

## A zh
好处是**独立的扩展和弹性**：计算可以缩至零或突增到数百个节点而无需移动数据；多个引擎（SQL、Spark、ML）读同一份文件；存储便宜、持久、基本无限。

创造了延迟问题：对象存储读是**网络上十几毫秒的首字节**对比本地 NVMe 微秒——所以每个成熟引擎都加**热数据的本地 SSD/内存缓存**和列式格式+元数据裁剪来尽量少读字节。适合分析；OLTP 仍想要计算旁的存储。
