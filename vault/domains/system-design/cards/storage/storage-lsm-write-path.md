---
id: storage-lsm-write-path
node: storage.internals.lsm
type: cloze
---
LSM-tree write path, in order: (1) append the write to the {{c1::WAL (sequential log, for crash recovery)}}; (2) insert it into the {{c2::memtable — an in-memory sorted structure such as a skip list or red-black tree}}; (3) when the memtable exceeds its size threshold, make it immutable, swap in a fresh one, and {{c3::flush it to disk as an SSTable (a sorted, immutable file)}}; (4) in the background, {{c4::compaction}} merge-sorts SSTables together, keeping only each key's newest version and discarding shadowed values. The user-visible write finishes after step (2) — everything that touches disk in bulk happens {{c5::sequentially}}, which is the source of LSM write throughput.

## zh
LSM-tree 写路径，按顺序：(1) 把写入追加到 {{c1::WAL（顺序日志，用于崩溃恢复）}}；(2) 把它插入 {{c2::memtable — 一个内存中的有序结构，如 skip list 或红黑树}}；(3) 当 memtable 超过大小阈值时，把它设为不可变、换上一个新的，并{{c3::把它 flush 到磁盘成为一个 SSTable（有序的不可变文件）}}；(4) 在后台，{{c4::compaction}} 把多个 SSTable 归并排序在一起，只保留每个 key 的最新版本、丢弃被覆盖的值。用户可见的写入在第 (2) 步之后就完成了 — 所有批量触盘的操作都是{{c5::顺序（sequentially）}}进行的，这正是 LSM 写吞吐的来源。
