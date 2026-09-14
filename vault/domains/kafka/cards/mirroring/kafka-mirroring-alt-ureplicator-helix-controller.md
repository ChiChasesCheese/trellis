---
id: kafka-mirroring-alt-ureplicator-helix-controller
node: mirroring.alternatives
type: qa
source: kafka-2e
---
## Q
uReplicator（Uber 开发的旧版 MirrorMaker 替代品）用什么机制取代了旧版 MirrorMaker 里「消费者群组自动再均衡」来分配分区，从而避免因为新增主题、重启实例等操作触发长时间停顿？这个方案带来了什么额外代价？

## A
uReplicator 引入 Apache Helix 作为一个高可用的**中心控制器**，专门负责维护需要镜像的主题列表，并把分区显式分配给各个 uReplicator 实例；管理员通过 REST API 增删主题，Helix 控制器计算好分配方案后推送给各实例，实例之间不需要像标准消费者群组那样互相协调、协商谁该消费哪个分区，只需被动监听 Helix 控制器发来的分配变更即可，从根本上避免了消费者再均衡及其造成的停顿。代价是整个方案多引入了 Helix 这样一个额外的分布式组件需要独立部署和运维，增加了系统复杂度。
