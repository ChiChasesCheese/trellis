---
id: clone-dml-during-clone-retention-zero
node: continuity.zero-copy-clone
type: qa
source: snowflake-docs
---
## Q
克隆一个大模式时报错说数据不可用，而其中几张表的 `DATA_RETENTION_TIME_IN_DAYS` 被设成了 0。原因是什么？该怎么做？

## A
克隆需要一段时间，Snowflake 试图克隆操作开始时刻的表数据；如果克隆期间源表发生了 DML，而保留期为 0 使旧版本数据被清除，克隆就拿不到开始时刻的数据而失败。做法：克隆期间尽量不对源对象执行 DML；或在克隆前把相关表的保留期临时设为 1，完成后再改回 0。
