---
id: problems-hotel-reservation-multirow-conditional-update-rollback
node: problems.commerce.hotel-reservation
type: qa
step: 4
tags: [grown]
---
## Q
A hotel reservation system books a 3-night stay with one multi-row `UPDATE ... WHERE date = ANY(:dates) AND booked_units < total_units*(1+overbook_pct)`. If only 2 of the 3 target nights satisfy that WHERE clause, does PostgreSQL fail the whole statement, and what must the application do to guarantee that this reservation succeeds or fails as one unit?

## A
No — PostgreSQL's UPDATE simply skips rows that don't match the WHERE clause and updates only the rows that do, reporting an affected-row count of 2 rather than raising an error. The application must check, inside the same database transaction, whether the affected-row count equals the number of nights requested, and explicitly ROLLBACK if it doesn't; the ROLLBACK undoes even the rows that individually passed their own capacity check, which is what actually delivers the 'the whole date range succeeds or fails together' guarantee that a single-row conditional update doesn't need to worry about.

## Q zh
酒店预订系统用一条多行 `UPDATE ... WHERE date = ANY(:dates) AND booked_units < total_units*(1+overbook_pct)` 来预订 3 个晚上。如果目标的 3 晚里只有 2 晚满足 WHERE 子句，PostgreSQL 会让整条语句失败吗？应用层必须做什么才能保证这笔预订整体成功或整体失败？

## A zh
不会——PostgreSQL 的 UPDATE 只会跳过不满足 WHERE 子句的行，只更新满足条件的那些行，返回的受影响行数是 2 而不是报错。应用层必须在同一个数据库事务内检查受影响行数是否等于请求的晚数，不等于就显式 ROLLBACK；这次 ROLLBACK 会撤销那些单独看已经通过自己容量检查的行，这才真正实现了「整段日期区间要么一起成功、要么一起失败」的保证——这一步是单行条件更新不需要操心的额外复杂度。
