---
id: hi-pt-distributed-file-system-11-erasure-coding
node: qb.sd.distributed-file-system.points
type: qa
step: 11
---
## Q
**分布式文件系统 · 纠删码**｜加分 · 出自：分布式文件系统 › 深入 7

分布式文件系统的冷数据想省空间，可以用纠删码（6+3）代替三副本。能省多少？代价是什么？

## A
**数字。** 6+3 开销 1.5 倍：200 PB 只需 300 PB，三副本要 600 PB，省 300 PB。

**代价。** 修复要读 6 个块，小范围读可能需要重建。

**适用。** 冷数据。
