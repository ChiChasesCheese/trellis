---
id: ddl-running-query-keeps-its-version
node: metadata.ddl-metadata-versioning
type: qa
tags: [grown]
---
## Q
一条长查询正在读表 t，这时另一个会话对 t 执行了 `ALTER TABLE t DROP COLUMN x`。正在跑的查询会出错吗？为什么？

## A
不会。DDL 并不就地修改数据，而是在元数据中提交一个新的表版本；正在执行的查询在开始时已经确定了要读取的表版本及其微分区（micro-partition）文件，这些不可变文件依然存在，查询按原版本读完即可。DDL 提交之后开始的查询才会看到没有 x 列的新版本。读写双方通过版本隔离，互不阻塞。
