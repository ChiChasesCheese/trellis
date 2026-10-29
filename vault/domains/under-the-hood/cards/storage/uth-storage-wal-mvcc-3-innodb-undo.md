---
id: uth-storage-wal-mvcc-3-innodb-undo
node: storage.wal-mvcc
type: qa
step: 3
---
## Q
**InnoDB：原地更新，旧版本放 undo 链**｜InnoDB · MySQL 8.4

InnoDB 同样是 MVCC，旧版本放在哪？一致性读（consistent read）怎样读到它们？

## A
**结构。** 聚簇索引里的行是最新版本，每行多 6 字节 `DB_TRX_ID`（最后改它的事务）和 7 字节 `DB_ROLL_PTR`（指向 undo 记录）。旧版本在回滚段的 undo 记录里，串成链。

**细节。**

- 读事务按读视图沿 `DB_ROLL_PTR` 往回走，直到找到可见的版本。
- 删除也是更新：先打删除标记，没有快照需要时由 purge 线程真正移除。

**坑。** 长事务让 undo 越积越多；官方建议定期提交，连只读事务也一样。

**为什么。** PostgreSQL 新旧版本都在表里（要 VACUUM）；InnoDB 表里只留最新版本，代价是读旧版本要回溯。

**对应 LeetCode：** LC 981 基于时间的键值存储 · LC 1146 快照数组
