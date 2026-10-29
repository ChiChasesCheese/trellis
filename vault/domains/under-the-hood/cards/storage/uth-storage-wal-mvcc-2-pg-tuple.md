---
id: uth-storage-wal-mvcc-2-pg-tuple
node: storage.wal-mvcc
type: qa
step: 2
---
## Q
**PostgreSQL：旧版本就留在表里**｜PostgreSQL · 18

PostgreSQL 里 `UPDATE` 一行，旧数据去哪了？读事务为什么不用等写事务？

## A
**结构。** 堆表里每个元组（tuple）带 23 字节的头：`t_xmin`（创建它的事务号）、`t_xmax`（删除或锁定它的事务号）、`t_ctid`（指向新版本）。`UPDATE` = 写一个新元组，并把旧元组的 `xmax` 设成当前事务。

**细节。**

- 读事务拿一个快照（snapshot），逐个元组判断：`xmin` 已提交且在快照之前、`xmax` 未提交或在快照之后，这个版本才可见。
- 没有任何快照还需要的旧版本叫死元组，由 `VACUUM` 回收。

**为什么。** 读不加锁、不阻塞写；代价是表会膨胀，必须靠 VACUUM 清理。

**对应 LeetCode：** LC 981 基于时间的键值存储 · LC 1146 快照数组
