---
id: reader-no-dml
node: sharing.reader-accounts
type: qa
source: snowflake-docs
---
## Q
合作方拿到只读账户（reader account）后，想把自己的一份 CSV 加载进去和共享数据做 JOIN。能做到吗？为什么？

## A
不能。只读账户里的用户只能查询通过该账户导入的共享数据，不能执行完整账户允许的 DML 类操作，比如数据加载、INSERT、UPDATE 等数据修改操作，所以无法把自己的数据加载进去做关联分析。需要与自有数据结合的合作方应开通自己的完整 Snowflake 账户，作为普通消费方接入 share。
