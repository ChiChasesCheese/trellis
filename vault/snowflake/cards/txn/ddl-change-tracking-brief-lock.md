---
id: ddl-change-tracking-brief-lock
node: txn.ddl-as-transaction
type: qa
source: snowflake-docs
---
## Q
对一张繁忙的表执行 `CREATE STREAM` 或 `ALTER TABLE ... SET CHANGE_TRACKING = TRUE`（开启变更追踪）时会加锁吗？哪些并发写入会被挡住？

## A
会，但通常只锁很短时间。开启 CHANGE_TRACKING 的 CREATE TABLE、CREATE DYNAMIC TABLE、CREATE STREAM 和 ALTER TABLE 会锁住底层表；表被锁期间只有 UPDATE 和 DELETE 这类 DML 会被阻塞，INSERT 不会被阻塞，因为 INSERT 只追加新分区而不改写现有数据。
