---
id: hi-c-sd-time-series-databases-n10-storage-engine
node: sd.deep-dives.time-series-databases.notes
type: qa
step: 9
---
## Q
**时序数据库 · 存储引擎如何拼起来**｜摘要 · 必会

一个典型时序存储引擎怎么把前面的积木组合起来？一次写入经过哪些步骤，文件里长什么样？

## A
- **写路径：** 先写预写日志（WAL，Write-Ahead Log）保证崩溃可恢复；同时写内存缓冲（按指标加标签组合组织，即 memtable）；缓冲满了就压缩后刷成不可变文件；后台压缩合并小文件并清除已删数据。
- **文件格式：** 文件头；每个序列一块一块存，块内时间戳用 delta-of-delta 加变长整数，数值用 XOR 压缩；文件尾部是索引（序列键到块偏移），再加文件尾。
- **查一个序列：** 先到索引（一次寻道），再到数据块（一次寻道），与文件多大无关，只要两次磁盘操作。
