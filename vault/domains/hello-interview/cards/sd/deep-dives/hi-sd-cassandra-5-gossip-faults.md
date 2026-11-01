---
id: hi-sd-cassandra-5-gossip-faults
node: qb.sd.notification-system-scale.pre-sd-deep-dives-cassandra
type: qa
step: 5
---
## Q
**Gossip 与容错：无单点**｜系统设计 · 深入专题

Cassandra 没有主节点，集群状态是怎么传播的？节点宕机时写入怎么办？

## A
**要点。** 任何节点都能当协调者（coordinator）接收客户端请求，再转给持有数据的副本。节点之间用 gossip（点对点传闻）交换存活状态与 schema：每个节点记录对方的 generation（启动时间戳）和 version（约每秒递增的逻辑时钟），用它忽略过期信息。gossip 对象偏向种子节点（seed），避免集群分裂成互不知晓的小团体。

**故障检测。** Phi Accrual 故障检测器：每个节点独立判断对方是否可用，判定失败就不再向其路由写入；但不会立即从环上摘除，要管理员改拓扑，以免短暂抖动引发数据重分布。

**暂存写入。** 提示移交（hinted handoff）：协调者替宕机节点暂存写入（hint），对方恢复时再投递。hint 寿命短；长期离线的节点靠重建或读修复（read repair）追平。

**为什么。** 没有主节点、没有单点，所以是偏可用性（AP）的数据库。
