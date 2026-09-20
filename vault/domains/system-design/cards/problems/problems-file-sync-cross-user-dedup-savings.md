---
id: problems-file-sync-cross-user-dedup-savings
node: problems.media.file-sync
type: qa
step: 2
tags: [grown]
---
## Q
In a file sync system where blocks are keyed by their SHA-256 content hash rather than by owner, why does storing blocks this way automatically deduplicate identical content uploaded by different users, and what fraction of raw storage growth might this save?

## A
Because the block's storage key is derived purely from its byte content (its hash), two different users uploading byte-identical content (a common installer, a shared template, a public dataset) produce the same hash and therefore reference the same stored block instead of each writing a separate copy; the block only needs one physical copy regardless of how many files or users reference it. Assuming roughly 30% of blocks across a large user base are byte-identical to blocks already stored by someone else, this content-addressed model can cut actual new storage writes by about 30% relative to a design that stores every user's blocks in an isolated per-owner namespace.

## Q zh
在一个块以其 SHA-256 内容哈希（而不是所有者）为键的文件同步系统中，为什么这种存储方式能自动对不同用户上传的相同内容去重？这大概能省下多大比例的原始存储增长？

## A zh
因为块的存储键完全由其字节内容（哈希值）派生，两个不同用户上传字节完全相同的内容（常见安装包、共享模板、公开数据集）会产生同一个哈希，从而引用同一个已存储的块，而不是各自写一份独立拷贝——无论多少文件或用户引用它，这个块只需要一份物理拷贝。假设在一个大用户群体中，约 30% 的块与其他人已存储的块字节完全相同，这种内容寻址模型相比「每个所有者独立命名空间存储」的设计，能把实际新增存储写入量减少约 30%。
