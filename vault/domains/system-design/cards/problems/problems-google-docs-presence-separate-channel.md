---
id: problems-google-docs-presence-separate-channel
node: problems.media.google-docs
type: qa
step: 6
tags: [grown]
---
## Q
In a collaborative document editor, why should cursor position and presence updates be broadcast through a completely separate channel from the document's edit-operation log, rather than being modeled as just another operation type in that log?

## A
A stale or dropped cursor update only costs a brief visual glitch, while a stale or lost text operation is data corruption — these two kinds of data have fundamentally different persistence, ordering, and loss-tolerance requirements. Routing presence through the same durable, strictly-ordered operation log as document edits would force cursor updates to pay for guarantees they don't need (durability, transformation, global ordering) and would pollute the version history with high-frequency, content-irrelevant records, so presence instead goes through a lightweight, best-effort, unordered publish-subscribe channel that can drop messages and scale independently.

## Q zh
在协同文档编辑器中，为什么光标位置和在线状态广播应该走一条与文档操作日志完全独立的通道，而不是把它建模成操作日志里的另一种操作类型？

## A zh
一次丢失或延迟的光标更新只造成短暂的视觉瑕疵，而一次丢失或过期的文本操作则是数据损坏——这两类数据在持久化、顺序、丢失容忍度上的要求根本不同。如果把在线状态也塞进和文档编辑共用的那条持久化、严格有序的操作日志，就会迫使光标更新为它并不需要的保证（持久性、转换、全局顺序）付出代价，还会用大量高频、与内容无关的记录污染版本历史，所以在线状态改走一条轻量、尽力而为、无需顺序、可以丢帧的发布订阅通道，能够独立于编辑路径横向扩展。
