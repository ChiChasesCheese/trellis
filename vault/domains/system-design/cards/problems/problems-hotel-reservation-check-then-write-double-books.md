---
id: problems-hotel-reservation-check-then-write-double-books
node: problems.commerce.hotel-reservation
type: qa
step: 3
tags: [grown]
---
## Q
In a hotel reservation system under PostgreSQL's default read-committed isolation, why does 'SELECT remaining capacity for each night, check it in application code, then UPDATE that night's booked-unit count' allow two concurrent bookings to jointly overbook a room-type's last available night, even though neither individual UPDATE conflicts with the other?

## A
Between the SELECT and the UPDATE there is no lock protecting the decision window: two concurrent transactions can both read the same 'remaining = 1' snapshot, each independently decide in application code that the night is bookable, and then both issue non-conflicting UPDATEs (each just increments booked_units by one). This is the write-skew anomaly — two transactions read a shared snapshot, make disjoint writes, and jointly violate an invariant that neither write alone violates. Serializable isolation would catch this, but the cheaper fix is to never split the check from the write: fold the capacity check directly into the UPDATE's own WHERE clause so the check and the write happen atomically.

## Q zh
在 PostgreSQL 默认的读已提交（read committed）隔离级别下，酒店预订系统里「先 SELECT 查每晚剩余库存、在应用层判断、再 UPDATE 已订数量」这种写法，为什么会让两笔并发预订共同超卖某个房型最后一晚的库存，即使两次 UPDATE 本身并不冲突？

## A zh
SELECT 和 UPDATE 之间没有任何锁保护这段决策窗口：两个并发事务可以都读到同一份「剩余 = 1」的快照，各自在应用层独立判断「这一晚可以订」，然后都发出互不冲突的 UPDATE（各自只是把 booked_units 加一）。这正是写偏斜（write skew）异常——两个事务基于同一份共享快照做出互不相交的写入，合并后共同违反了一个任何一次写单独看都不违反的不变量。可串行化隔离能挡住这种情况，但更便宜的修法是从一开始就不要把检查和写入拆成两步：把容量检查直接写进 UPDATE 自己的 WHERE 子句，让检查和写入原子地一起发生。
