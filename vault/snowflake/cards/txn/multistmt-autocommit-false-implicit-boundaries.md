---
id: multistmt-autocommit-false-implicit-boundaries
node: txn.multi-statement-transactions
type: cloze
source: snowflake-docs
---
当 `AUTOCOMMIT = FALSE` 时，Snowflake 的隐式事务边界：
- 隐式 BEGIN：事务结束后的{{c1::第一条 DML 语句}}；
- 隐式 COMMIT：执行{{c2::DDL 语句}}，或执行 {{c3::`ALTER SESSION SET AUTOCOMMIT`（即使值未改变）}}；
- 隐式 ROLLBACK：{{c4::会话结束}}，或{{c5::存储过程结束时仍有活跃事务}}。
