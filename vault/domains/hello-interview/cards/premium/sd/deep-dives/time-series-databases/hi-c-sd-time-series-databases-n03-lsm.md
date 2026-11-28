---
id: hi-c-sd-time-series-databases-n03-lsm
node: sd.deep-dives.time-series-databases.notes
type: qa
step: 3
---
## Q
**时序数据库 · LSM 树**｜摘要 · 必会

LSM 树（Log-Structured Merge Tree）怎么把随机写变成顺序写？写入、落盘、合并各做什么，代价是什么？

## A
- **第一步，写内存：** 数据先进内存缓冲区 memtable，用红黑树或跳表保持有序，写入只碰内存，所以极快。保持有序是为了落盘后的文件也有序。
- **第二步，落盘：** memtable 写满后顺序写成不可变的有序文件 SSTable（Sorted String Table），然后清空 memtable 接收新数据。有序文件支持二分查找、范围扫描，还能用归并排序合并。
- **第三步，后台压缩（compaction）：** 文件越积越多，读要翻多个文件；后台把小 SSTable 合并成大的，同时丢掉重复值和删除标记（tombstone）。
- **好处：** 写不被读阻塞，读写分离，所以能持续高写入。
- **代价：** 读可能要查多个 SSTable；写放大（write amplification）：同一份数据在压缩中被反复重写。写多读少、能接受读变慢时才选它。
