---
id: distributed-or-set
node: distributed.crdt
type: qa
---
## Q
Replicated set: replica A removes element x while replica B concurrently re-adds x. Why do naive sets and 2P-Sets get this wrong, and how does an OR-Set resolve it?

## A
- **Naive set**: add/remove don't commute, so replicas that see them in different orders diverge — no well-defined answer.
- **2P-Set**: removals go to a tombstone set that wins forever — once removed, x can **never be re-added**.
- **OR-Set (observed-remove)**: every add attaches a **unique tag**; remove deletes only the tags the remover had *observed*. B's concurrent re-add carries a fresh tag A never saw, so it survives the merge — **add wins over concurrent remove**, and re-adding after removal works.

Cost: tag/tombstone metadata grows with operations and needs eventual compaction. LWW-element-sets avoid the metadata but inherit timestamp data loss ([[distributed-lww-danger]]).

## Q zh
一个复制集合：副本 A 移除元素 x，同时副本 B 并发地重新加入了 x。为什么朴素的集合和 2P-Set 会处理错？OR-Set 又是怎样解决这个问题的？

## A zh
- **朴素集合**：add/remove 不满足可交换性，所以以不同顺序看到它们的副本会发散——没有一个良定义的答案。
- **2P-Set**：移除操作进入一个永远生效的墓碑集合——一旦被移除，x 就**再也不能被重新加入**。
- **OR-Set（observed-remove）**：每次 add 都附带一个**唯一标签**；remove 只删除移除者*当时观察到的*那些标签。B 并发的重新加入带着一个 A 从未见过的全新标签，所以它能在合并后存活下来——**add 战胜并发的 remove**，移除之后重新加入也能正常工作。

代价：标签/墓碑元数据会随操作增多而增长，需要最终做压缩。LWW-element-set 避开了这份元数据，但继承了时间戳带来的数据丢失问题（[[distributed-lww-danger]]）。
