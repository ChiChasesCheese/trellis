%% trellis:begin %%
# WAL 与 MVCC
*数据库与搜索引擎*

先写日志再改数据页，崩溃后重放；MVCC 用版本链让读不阻塞写（InnoDB 的 undo 链、PostgreSQL 的元组多版本）。

## Cards (4)
1. [[uth-storage-wal-mvcc-1-write-ahead]]
2. [[uth-storage-wal-mvcc-0-why-mvcc]]
3. [[uth-storage-wal-mvcc-2-pg-tuple]]
4. [[uth-storage-wal-mvcc-3-innodb-undo]]
%% trellis:end %%

## Notes
