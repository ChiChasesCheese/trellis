---
id: hi-c-sd-cassandra-n03-primary-key
node: sd.deep-dives.cassandra.notes
type: qa
step: 3
---
## Q
**Cassandra · 主键 = 分区键 + 聚簇键**｜摘要 · 必会

Cassandra 的主键由什么组成？分区键和聚簇键各决定什么？括号怎么写？

## A
- **分区键（partition key）：** 一列或多列，决定这一行落在哪个分区、也就是哪些节点上。**同一分区键的行物理上放在一起。**
- **聚簇键（clustering key）：** 零列或多列，决定同一分区内行的排序，让按顺序读取变得高效。
- **写法：** `PRIMARY KEY ((a, b), c)` 表示 a 与 b 合成复合分区键，c 是聚簇键；`PRIMARY KEY (a, b, c)` 表示 a 是分区键，b、c 都是聚簇键。内层括号是分区键的边界。
- **与 DynamoDB 的对应：** 分区键对应分区键，聚簇键对应排序键，概念几乎一一对应。
- **后果：** 查询必须给出完整的分区键才能高效，因为只有这样才能定位到节点；聚簇键决定范围查询和排序能否直接读取。
