---
id: storage-sstable-structure
node: storage.internals.lsm
type: qa
---
## Q
What exactly makes an SSTable's *sorted* order so valuable that LSM engines pay compaction forever to maintain it? Give the three concrete capabilities sorting buys inside one file.

## A
- **A sparse index suffices.** Because keys are in order, the in-memory index needs only one entry per block (every few KB), not per key: find the two index entries bracketing your key, read that one block, scan it. Contrast a hash-based log index, which needs *every* key in memory.
- **Efficient merging.** N sorted files merge with a linear mergesort-style pass — look at the head of each, copy the smallest, repeat. That's what makes compaction (and flush-time dedup of key versions) affordable at all.
- **Compression-friendly blocks.** Each block is compressed as a unit before hitting disk; adjacent keys share structure, so sorted blocks compress well — shrinking both disk usage and I/O bandwidth per read.

Bonus: sorted files give range scans a contiguous slice per file — the piece Bloom filters can't help with.

## Q zh
SSTable 的*有序*到底有什么价值，让 LSM 引擎愿意永远支付 compaction 的代价来维持它？给出有序性在单个文件内换来的三项具体能力。

## A zh
- **稀疏索引就够了。** 因为 key 有序，内存索引只需每个块（每隔几 KB）一个条目，而不是每个 key 一个：找到夹住目标 key 的两个索引条目，读那一个块，在块内扫描。对比基于哈希的日志索引，它需要把*所有* key 放进内存。
- **高效归并。** N 个有序文件用一次线性的、归并排序式的扫描即可合并 — 看每个文件的头部，拷贝最小的，重复。这正是 compaction（以及 flush 时对 key 版本去重）在成本上可行的原因。
- **对压缩友好的块。** 每个块在落盘前作为一个单元压缩；相邻 key 结构相似，所以有序的块压缩率好 — 同时缩小磁盘占用和每次读取的 I/O 带宽。

附加：有序文件让范围扫描在每个文件里对应一段连续切片 — 这是 Bloom filter 帮不上忙的那部分。
