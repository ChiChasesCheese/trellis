---
id: sproc-vs-udf-capability
node: openplatform.stored-procedure-sandboxing
type: qa
tags: [grown]
---
## Q
存储过程（stored procedure）和 UDF 都能用 Python 写，为什么需要执行 DDL/DML 的逻辑（如建表、循环执行 MERGE）必须用存储过程？

## A
UDF 在查询内部逐行或逐批被调用，必须表现为无副作用的函数，不能在执行中发出新的 SQL 语句。存储过程通过 `CALL` 独立调用，拿到一个 Snowpark session，可以按过程逻辑依次执行任意 SQL（DDL、DML、事务控制）并处理结果，适合编排多步管理任务。因此“对数据逐行计算”用 UDF，“编排一系列数据库操作”用存储过程。
