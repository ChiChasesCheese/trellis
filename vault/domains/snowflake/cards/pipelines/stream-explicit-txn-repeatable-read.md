---
id: stream-explicit-txn-repeatable-read
node: pipelines.stream-consumption-and-offset-advance
type: qa
source: snowflake-docs
---
## Q
需要用同一批流变更分别 INSERT 到两张目标表。为什么要把两条语句包在 `BEGIN … COMMIT` 中？事务期间对源表的并发写入会怎样？

## A
若不包在事务里，第一条自动提交的 DML 就会消费全部变更并前移偏移量，第二条读到的是空集或新的增量。在显式事务中，流支持可重复读（repeatable read）隔离：事务内所有语句看到的都是从流当前位置到事务开始时间的同一批记录，流在被 DML 使用后会被锁定。其他事务在此期间对源表的 DML 仍会被变更追踪记录，但要等本事务提交、现有变更被消费后，才出现在流的下一次增量中。
