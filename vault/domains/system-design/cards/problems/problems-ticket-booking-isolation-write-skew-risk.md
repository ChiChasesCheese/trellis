---
id: problems-ticket-booking-isolation-write-skew-risk
node: problems.commerce.ticket-booking
type: qa
step: 3
tags: [grown]
---
## Q
Why is read-committed isolation sufficient for a ticket booking system's single-statement conditional UPDATE on a seat row, but not sufficient if the hold logic were instead implemented as a separate SELECT of available seats followed by an INSERT?

## A
A single conditional UPDATE re-evaluates its WHERE clause against the latest committed state at execution time, so a concurrent transaction can never read a stale 'available' value under read committed — there is no window for an anomaly. But splitting it into 'read a set of available seats, then write to one of them' reintroduces the classic write-skew anomaly (two transactions independently read the same snapshot, each picks a seat they believe is free, and both commit), which requires serializable isolation or explicit row locks to prevent.

## Q zh
为什么票务预订系统中对一个座位行的单语句条件更新，用读已提交（read committed）隔离级别就足够安全，但如果把占座逻辑拆成先 SELECT 查可用座位、再对其中一个做 INSERT，就不够了？

## A zh
单语句条件更新在执行时会针对最新的已提交状态重新求值 WHERE 子句，所以在读已提交级别下并发事务永远不会读到过期的 'available' 值——不存在产生异常的窗口。但如果拆成"先读一批可用座位，再写其中一个"两步，就会重新引入经典的写偏斜（write skew）异常（两个事务各自基于同一份快照读取，各自认为选中的座位是空的，然后都提交成功），这时必须用可串行化（serializable）隔离级别或显式行锁才能防止。
