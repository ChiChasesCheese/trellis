---
id: problems-meeting-scheduler-room-vs-calendar
node: problems.booking.meeting-scheduler
type: qa
step: 2
tags: [grown]
---
## Q
会议室预订设计里，为什么“这间房现在被谁占着”这份状态要放在 `RoomCalendar` 上，而不是放在 `Room` 本身？

## A
`Room` 描述的是容量、设备这些几乎不变的物理事实；“忙闲”是每分钟都可能变化、需要加锁保护的状态。把两种生命周期完全不同的数据塞进同一个类，要么让不变的数据跟着变化的状态一起被复制，要么让可变状态失去清晰的归属和锁的边界。`RoomCalendar` 因此是本设计里唯一持有占用状态的对象，一间房一把私有锁，不同房间之间零共享、天然不互相阻塞。
