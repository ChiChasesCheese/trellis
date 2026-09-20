---
id: problems-meeting-scheduler-lock-nesting-order
node: problems.booking.meeting-scheduler
type: qa
step: 8
tags: [grown]
---
## Q
会议室预订设计里，`RoomCalendar` 和它挂着的每条 `RecurringSeries` 各有自己的锁，为什么这样不会造成锁顺序死锁？

## A
调用链永远是单方向的：`RoomCalendar` 的方法在持有自己的锁期间可能去调用某条周期系列的方法（因而再拿一次那条系列自己的锁），但周期系列的任何方法都不会反过来去拿 `RoomCalendar` 的锁。固定的单向嵌套顺序——房间锁总在外层、系列锁总在内层，从不反过来——本身就排除了两个线程互相等待对方锁的环形等待条件，这条纪律比选用哪种锁类型更重要。
