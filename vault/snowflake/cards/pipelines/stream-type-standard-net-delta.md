---
id: stream-type-standard-net-delta
node: pipelines.stream-types
type: qa
source: snowflake-docs
---
## Q
在两次消费之间，一行先被 INSERT 又被 DELETE。标准流（standard stream）和仅追加流（append-only stream）分别会返回这一行吗？为什么？

## A
标准流（又称 delta 流）不会返回：它追踪所有 DML（插入、更新、删除，含 TRUNCATE），并对变更集中的插入行和删除行做连接，计算行级净变化，插入后又删除的行净效果为零。仅追加流会返回这次插入：它只追踪行插入，完全不记录更新、删除和截断。
