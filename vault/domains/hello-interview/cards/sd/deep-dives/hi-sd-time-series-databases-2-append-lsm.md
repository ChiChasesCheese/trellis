---
id: hi-sd-time-series-databases-2-append-lsm
node: qb.sd.top-k-counts.pre-sd-deep-dives-time-series-databases
type: qa
step: 2
---
## Q
**追加写和 LSM 树为什么写得快**｜系统设计 · 深入专题

时序数据库的写入吞吐为什么高？追加写（append-only）与 LSM 树（Log-Structured Merge Tree）的机制是什么，代价是什么？

## A
**追加写。** 传统数据库更新一行要：定位磁盘位置、读出旧数据、内存修改、写回，这是随机 I/O，机械盘每秒只有 100 到 200 次操作，SSD 随机也不如顺序。追加写只把新点写到文件末尾，没有寻道，顺序写 SSD 每秒能达数十万次，机械盘也有数万次。

**LSM 树。** 把随机写变成顺序写，再在后台整理：
1. 写入先进内存缓冲（memtable），用红黑树或跳表保持有序，写很快
2. 缓冲满了，按序整体刷到磁盘，形成不可变的有序文件 SSTable，是一次顺序写
3. **压缩归并并清墓碑：** 后台压缩（compaction）把小文件归并成大文件，去掉重复和删除标记（tombstone）

保持有序，是为了点查可以二分、范围查询相邻、压缩时能用归并排序合并。读写分离，写永远不会被读阻塞。

**取舍。** 代价是读可能要查多个 SSTable，以及写放大（数据在压缩中被重写多次）。写多读少、愿意用读性能换写性能时选它。Cassandra、LevelDB 也是这套思路。
