---
id: hi-c-sd-cassandra-n06-replication
node: sd.deep-dives.cassandra.notes
type: qa
step: 6
---
## Q
**Cassandra · 复制：副本放在哪、两种策略**｜摘要 · 必会

Cassandra 怎么选择一份数据的副本放在哪些节点？NetworkTopologyStrategy 和 SimpleStrategy 的区别是什么？

## A
- **选址：** 键哈希到环上的某个 vnode 后继续顺时针扫描，找到副本数所需的节点；若遇到和已选节点在同一台物理机上的 vnode 就跳过，避免一台机器宕机就同时丢多个副本。
- **复制因子（replication factor）：** 每份数据存几份，在键空间上配置。
- **SimpleStrategy：** 只顺时针扫描，不知道机房和机架，适合测试和简单部署。
- **NetworkTopologyStrategy：** 生产推荐。能感知数据中心和机架，让副本分散到不同机架和机房，并可按数据中心分别指定副本数，如 dc1 放 3 份、dc2 放 2 份。
- **目的：** 让副本在物理上尽量隔开，一次真实故障（机架断电、机房故障）不会同时带走大多数副本。
