---
id: hi-c-sd-cassandra-x03-low-cardinality
node: sd.deep-dives.cassandra.exam
type: qa
step: 3
---
## Q
**Cassandra · 低基数分区键**｜考点 · 必会

用户表设计成 `PRIMARY KEY (country, user_id)`，为了"按国家列出用户"。上线后会遇到什么问题？

## A
- **热点与超大分区：** 国家数量很少（约两百个），分区键基数太低；大国的上亿用户全在一个分区，由同一组存放副本的节点承担所有读写，既是热点，也是巨型分区。
- **负载不均：** 集群再扩容也没用，因为一个分区不能被拆开到更多节点。
- **改法一：** 如果真有此查询，加一个复合分区键 `(country, bucket)`，用户按 `hash(user_id) % 桶数` 分到多个桶，读取时并发查询所有桶后合并。
- **改法二：** 先确认是否真需要此查询；用户主表以 `user_id` 做分区键，列表需求可交给搜索引擎。
