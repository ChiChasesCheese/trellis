---
id: distributed-index-write-amplification
node: distributed.partitioning.indexes
type: cloze
---
Write amplification from global secondary indexes: inserting one row with k global indexes costs {{c1::1 + k writes, and each index write lands on a different partition (usually a different node) than the base row}}. Updating a row is worse than inserting it, because for each index whose indexed column changed you must {{c2::delete the entry under the old term and insert one under the new term — 2 index writes per changed indexed column, in two different index partitions}}. This is why the standard guidance is {{c3::index only the attributes you actually query on, and project only the attributes the query needs (DynamoDB KEYS_ONLY / INCLUDE beat ALL, since every projected attribute is copied on every write)}}. It is also why the writes cannot be transactional with the base row at scale: {{c4::making them atomic would require a distributed transaction across partitions on every single write, so systems make the index eventually consistent instead}}.

## zh
global secondary index 带来的写放大：插入一行、带 k 个 global index，代价是{{c1::1 + k 次写，而且每次 index 写落在与 base row 不同的 partition（通常是不同节点）上}}。更新一行比插入更糟，因为对每个被索引列发生了变化的 index，你必须{{c2::在旧 term 下删掉条目、再在新 term 下插入一条——每个变化的被索引列 2 次 index 写，落在两个不同的 index partition 上}}。所以标准建议是{{c3::只给你真正会查询的属性建索引，并且只投影查询需要的属性（DynamoDB 的 KEYS_ONLY / INCLUDE 优于 ALL，因为每个被投影的属性在每次写时都要复制一遍）}}。这也是为什么上了规模之后这些写没法和 base row 放进同一个事务：{{c4::要做到原子，就得在每一次写上都跨 partition 做一次分布式事务，所以系统改为让 index 最终一致}}。
