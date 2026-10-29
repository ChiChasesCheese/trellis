---
id: uth-storage-wal-mvcc-1-write-ahead
node: storage.wal-mvcc
type: qa
step: 1
---
## Q
**WAL：先写日志，再改数据页**｜SQLite · 3.53 / PostgreSQL · 18

数据库提交事务时，只把日志落盘，数据页稍后再写。崩溃之后靠什么恢复？

## A
**结构。** 预写日志（WAL）：改动先按顺序追加到日志，提交就是追加一条提交记录；数据页留在原处，由检查点（checkpoint）批量写回。崩溃后从最近的检查点开始重放日志。

**细节。**

- SQLite 的 WAL 模式：写者只往 WAL 末尾追加；WAL 满 1000 页自动做一次检查点。
- PostgreSQL 的 `checkpoint_timeout` 默认 5 分钟。

**坑。** 页写到一半断电（撕裂页）：PostgreSQL 默认 `full_page_writes = on`，检查点后每页第一次被改，就把整页写进 WAL。

**为什么。** 随机改页变成顺序追加，提交只要一次顺序写。

**对应 LeetCode：** 无直接对应的题（崩溃恢复）
