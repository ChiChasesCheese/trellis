---
id: hi-c-sd-zookeeper-n22-infra-problems
node: sd.deep-dives.zookeeper.notes
type: qa
step: 22
---
## Q
**ZooKeeper · 适用场景：设计分布式消息队列这类基础设施**｜摘要 · 追问

设计分布式消息队列时，ZooKeeper 承担哪些协调功能？

## A
- **broker 注册：** 加入集群时在 ZooKeeper 登记，其他组件据此发现。
- **主题元数据：** 创建主题时把分区数和副本数写进 ZooKeeper。
- **分区选主：** 同一分区只能有一个 broker 做领导者。常见做法是用临时节点抢占选出一个控制器（谁先创建成功谁当），再由控制器为每个分区指定领导者并写回 ZooKeeper；也可以每个分区各用"顺序加临时"节点选主。
- **消费者组：** 早期做法是把成员关系与分区分配存在 ZooKeeper，成员变动时触发重新平衡；Kafka 0.9 之后改由 broker 上的组协调器管理。
- **故障检测：** broker 崩溃，会话过期，节点消失，触发它所负责分区的重新分配，这是最重要的一环。
- **历史：** Kafka 多年就是这样做的，直到 KRaft；HBase、Hadoop、Solr 也类似。
- **相关题型：** 分布式任务调度器同样需要领导者和协调。
