---
id: hi-c-sd-zookeeper-n20-limits
node: sd.deep-dives.zookeeper.notes
type: qa
step: 19
---
## Q
**ZooKeeper · ZooKeeper 的三大局限**｜摘要 · 必会

基础设施设计题里该怎样说明 ZooKeeper 的缺点？

## A
- **热点（hot spotting）：** 许多客户端监视同一个 ZNode（选主、锁常见）时，服务器要发出大量通知；聊天例子里百万用户同时上线，热门节点会成为瓶颈。
- **性能：** 写要经过领导者传播给多数，代价高；数据放在内存里，容量有限，ZNode 要小于 1 MB，数据集要能装进内存。
- **运维复杂：** 要仔细配置 Java 参数、磁盘布局，并持续监视超时和连接。有一句话："用起来简单，运维起来复杂。"
- **何时考虑替代：** 需要存大量数据、极高写负载，或要尽量降低运维复杂度时。
