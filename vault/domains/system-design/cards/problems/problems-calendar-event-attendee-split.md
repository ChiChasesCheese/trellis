---
id: problems-calendar-event-attendee-split
node: problems.realtime.calendar
type: qa
step: 1
tags: [grown]
---
## Q
In a calendar system's data model, why should an event's core fields (organizer-controlled: time, location, recurrence rule) and its attendee list be stored as two separate tables rather than embedding the attendee array inside the event record?

## A
Embedding attendees inside the event record means every attendee's RSVP update requires a read-modify-write on the same document that the organizer's edits to time/location also write to, forcing two unrelated kinds of writes to contend for the same row's lock. Splitting them into an Event table (organizer-controlled fields only) and an Attendee table (one row per user-event relationship) lets an attendee's RSVP touch only their own row, never contending with the organizer's edits, and lets a 'my calendar' query hit the Attendee table directly by user id without needing a separate reverse index.

## Q zh
在日历系统的数据模型里，为什么事件的核心字段（组织者控制的：时间、地点、循环规则）和参会人列表应该存成两张独立的表，而不是把参会人数组内嵌在事件记录里？

## A zh
把参会人内嵌在事件记录里，意味着每一次参会人的 RSVP 更新都要对组织者编辑时间/地点时写入的同一份文档做读-改-写，迫使两类完全不相关的写操作争抢同一行的锁。拆成 Event 表（只存组织者控制的字段）和 Attendee 表（每行代表一个用户-事件关系）之后，参会人的 RSVP 只触碰自己的那一行，永远不会和组织者的编辑产生争用，而「我的日历」这类查询可以直接按用户 id 查 Attendee 表，不需要额外维护一份反向索引。
