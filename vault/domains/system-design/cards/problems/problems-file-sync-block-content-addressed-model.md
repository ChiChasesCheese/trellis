---
id: problems-file-sync-block-content-addressed-model
node: problems.media.file-sync
type: qa
step: 3
tags: [grown]
---
## Q
In a file sync system's data model, why is a Block keyed by its content hash and referenced by multiple FileVersion records (via an ordered blockIds list), rather than each FileVersion owning a private copy of its bytes?

## A
Keying blocks by content hash means identical content — whether from two versions of the same file that only changed a small part, or from two different files entirely — is stored exactly once and simply referenced by however many FileVersion records need it, with a refCount tracking how many references still exist so unreferenced blocks can eventually be garbage collected. If each FileVersion instead embedded its own private copy of the bytes, every new version of a large file would duplicate the storage of every unchanged block, defeating both the delta-sync bandwidth savings and cross-user deduplication that the content-addressed model provides for free.

## Q zh
在文件同步系统的数据模型中，为什么 Block 以内容哈希为键、被多个 FileVersion 记录（通过一个有序的 blockIds 列表）引用，而不是每个 FileVersion 各自拥有一份私有的字节拷贝？

## A zh
以内容哈希为键存储块，意味着相同的内容——无论是同一文件只改了一小部分的两个版本，还是完全不同的两个文件——都只存一份，被需要它的任意数量 FileVersion 记录引用，用 refCount 跟踪还有多少引用存在，没有引用的块最终可以被垃圾回收。如果每个 FileVersion 都各自内嵌一份私有字节拷贝，一个大文件的每个新版本都会把所有未变化的块重复存一遍，白白丢掉了内容寻址模型本该免费获得的增量同步带宽节省和跨用户去重收益。
