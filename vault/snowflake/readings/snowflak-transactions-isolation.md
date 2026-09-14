---
nodes:
- txn.acid-guarantees
- txn.multi-statement-transactions
- txn.ddl-as-transaction
- txn.snapshot-isolation
title: 事务、隐式提交与 READ COMMITTED 隔离级别
corpus: snowflake-docs
section: 16-transactions
url: https://docs.snowflake.com/en/sql-reference/transactions
tags:
- canonical
---

# 事务、隐式提交与 READ COMMITTED 隔离级别

Snowflake 保证 ACID:一组语句要么全部提交、要么全部回滚,且从不支持嵌套事务。显式事务用 BEGIN/COMMIT/ROLLBACK 界定,AUTOCOMMIT 默认开启时每条语句自成一个隐式单语句事务。DDL 语句永远自成一个独立事务:执行 DDL 会先隐式提交当前活跃事务,再单独执行并立即提交自己,因此 DDL 语句本身无法被回滚——这也是模式变更能对读者呈现为原子、瞬时切换的原因。隔离级别为 READ COMMITTED:一条语句只能看到该语句开始前已提交的数据,同一事务内前一条语句的未提交修改则对后续语句可见。读完能解释为什么在一个事务里连续查询同一张表,两次结果可能不同。
