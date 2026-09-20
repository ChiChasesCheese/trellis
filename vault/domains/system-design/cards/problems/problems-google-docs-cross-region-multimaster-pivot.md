---
id: problems-google-docs-cross-region-multimaster-pivot
node: problems.media.google-docs
type: qa
step: 8
tags: [grown]
---
## Q
In a collaborative document editor built around one authoritative ordering server per document, what architectural change would be required to support millisecond-latency multi-master editing across two continents, and why is it a reconsideration of the core design rather than an incremental scale-out?

## A
A single-authority ordering node inherently requires every editor's operations to round-trip to that one node to be sequenced, so editors far from it always pay cross-region network latency no matter how many machines are added elsewhere. Supporting true multi-master editing across regions would require reconsidering the operational-transformation choice itself and moving toward a CRDT-based model, accepting its position-identifier and tombstone metadata overhead in exchange for convergence without any single coordinating node — this is a change to which merge algorithm the whole system is built on, not something achieved by scaling the existing OT server tier.

## Q zh
在一个以「每篇文档一个权威排序服务器」为核心的协同文档编辑器里，要支持跨两个大洲、毫秒级延迟的多主编辑，需要什么样的架构改变，为什么这是对核心设计的重新权衡而不是增量扩容？

## A zh
单一权威排序节点本质上要求每个编辑者的操作都要往返到那一个节点才能被排序，所以离它远的编辑者无论在别处加多少机器都始终要承受跨区域网络延迟。要真正支持跨区域多主编辑，需要重新评估操作转换这个算法选择本身，转向基于 CRDT 的模型，接受其位置标识符和墓碑带来的元数据开销，换取不依赖任何单一协调节点的收敛能力——这是对整个系统所依赖的合并算法的改变，不是靠扩容现有 OT 服务器层就能达成的。
