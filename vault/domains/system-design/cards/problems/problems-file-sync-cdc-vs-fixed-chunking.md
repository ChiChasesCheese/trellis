---
id: problems-file-sync-cdc-vs-fixed-chunking
node: problems.media.file-sync
type: qa
step: 4
tags: [grown]
---
## Q
In a file sync system, why does fixed-size chunking cause a 'cascading hash invalidation' when bytes are inserted in the middle of a file, and how does content-defined chunking (CDC) avoid it?

## A
With fixed-size chunking, block boundaries are determined purely by byte offset (every 4MB, say); inserting even a few bytes shifts every subsequent boundary, so every block from the insertion point onward gets a different hash even though most of their actual content is unchanged, forcing all of them to be re-uploaded. Content-defined chunking instead places boundaries at positions determined by a rolling hash (e.g. a Rabin fingerprint) over the content itself, so an insertion only affects the one or two blocks immediately around it — boundaries further along the file re-synchronize with the content and stay unchanged, at the cost of the client having to compute the rolling hash over every byte instead of just counting offsets.

## Q zh
在文件同步系统中，为什么固定大小分块在文件中间插入字节时会引发「级联哈希失效」？内容定义分块（CDC）是如何避免这个问题的？

## A zh
固定大小分块的块边界完全由字节偏移量决定（比如每 4MB 一块）；即使只插入几个字节，之后所有的块边界都会整体偏移，导致插入点之后的每个块都得到不同的哈希，即使它们的实际内容大部分没变，也会被迫全部重新上传。内容定义分块则用对内容本身计算的滚动哈希（如 Rabin 指纹）来确定边界位置，所以插入只影响紧邻插入点的一两个块——更靠后的边界会随内容重新对齐、保持不变，代价是客户端要对每个字节计算滚动哈希，而不是简单地按偏移量计数。
