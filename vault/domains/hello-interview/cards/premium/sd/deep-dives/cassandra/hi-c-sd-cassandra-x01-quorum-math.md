---
id: hi-c-sd-cassandra-x01-quorum-math
node: sd.deep-dives.cassandra.exam
type: qa
step: 1
---
## Q
**Cassandra · 读写级别组合的一致性**｜考点 · 必会

复制因子为 3，下面哪些组合能保证读到最近一次成功的写入：写 QUORUM 读 QUORUM；写 ONE 读 ALL；写 ONE 读 ONE；写 ALL 读 ONE？再说明各自可用性代价。如果改为复制因子 5，QUORUM 是几？

## A
- **判据：** 读个数 + 写个数 > 复制因子才保证有重叠节点。
- **写 QUORUM 读 QUORUM：** 2 + 2 > 3，保证；容忍任一个副本宕机，这是最常用的平衡。
- **写 ONE 读 ALL：** 1 + 3 > 3，保证；但任一副本宕机，读就失败。
- **写 ALL 读 ONE：** 3 + 1 > 3，保证；但任一副本宕机，写就失败。
- **写 ONE 读 ONE：** 1 + 1 ≤ 3，不保证，可能读到旧值，换来最低延迟和最高可用。
- **复制因子 5：** QUORUM 是 5/2 + 1 = 3，可容忍两个副本不可用。
