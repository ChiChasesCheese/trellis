---
id: uth-storage-lsm-1-write-path
node: storage.lsm
type: qa
step: 1
---
## Q
**LSM 写路径：内存表、SST、分层**｜RocksDB · v10.9

RocksDB 写一条数据时发生了什么？数据怎样从内存一路沉到最底层？

## A
**结构。** 写先追加到 WAL（顺序写，崩溃恢复用），再插入内存表（memtable，跳表）。内存表满 64 MB（`write_buffer_size`）就冻结，刷成一个有序、不可变的文件 SST，放进第 0 层（L0）。

**细节。**

- L0 的文件之间键范围会重叠；攒够 4 个（`level0_file_num_compaction_trigger`）就合并进 L1。
- 默认 7 层，每层目标大小是上一层的 10 倍（`max_bytes_for_level_multiplier`）。
- 合并（compaction）= 多个有序文件做多路归并，同一个 key 只留最新的。

**为什么。** 随机写变成顺序追加和顺序合并，比 B+ 树原地改页更贴合磁盘的顺序带宽。

**对应 LeetCode：** LC 23 合并 K 个升序链表 · LC 21 合并两个有序链表
