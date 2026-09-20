---
id: problems-ticket-booking-seat-state-conditional-update
node: problems.commerce.ticket-booking
type: qa
step: 2
tags: [grown]
---
## Q
In a ticket booking system, what single SQL pattern lets a seat's available→held transition succeed atomically without holding a cross-request lock or relying on a background cron job to expire stale holds?

## A
A conditional UPDATE whose WHERE clause checks both current availability and lazy expiry in one statement: `UPDATE seats SET status='held', expires_at=now()+interval '10 minutes' WHERE status='available' OR (status='held' AND expires_at < now())`. The database's row-level write lock is held only for the statement's execution, rows affected = 1 means success and 0 means someone else already holds it; a low-priority background job may still archive long-expired rows, but it never carries correctness responsibility.

## Q zh
在票务预订系统中，用什么样的一条 SQL 能让座位从 available 到 held 的转移在不持有跨请求锁、也不依赖后台 cron 任务清理过期占座的情况下原子地成功？

## A zh
一条 WHERE 子句里同时检查当前可用性和惰性过期的条件更新：`UPDATE seats SET status='held', expires_at=now()+interval '10 minutes' WHERE status='available' OR (status='held' AND expires_at < now())`。数据库的行级写锁只在语句执行期间短暂持有，受影响行数为 1 表示抢到，为 0 表示已被别人占用；低优先级的后台任务仍可以定期归档长期过期的行，但它从不承担正确性职责。
