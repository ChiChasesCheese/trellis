---
id: problems-hotel-reservation-per-night-inventory-model
node: problems.commerce.hotel-reservation
type: qa
step: 2
tags: [grown]
---
## Q
In a hotel/marketplace reservation system, why is 'one row per room-type per night, with a total-units and booked-units counter' usually preferred over 'one row per physical room instance with a date-range exclusion constraint', even though PostgreSQL directly supports the latter via `EXCLUDE USING GIST (during WITH &&)`?

## A
A range-exclusion-constraint row per physical unit only enforces 'no two overlapping bookings on the SAME unit' — it can't express pooled capacity like '50 interchangeable rooms, sell up to 50 total' without creating and maintaining 50 separate constrained rows, and it binds a guest to a specific physical unit before check-in, which can produce a false 'fully booked' result when one specific unit is taken but an equivalent one is free. A per-room-type-per-night counter row lets any of the interchangeable units satisfy a booking, maximizing bin-packing efficiency; the exclusion-constraint model is reserved for cases that genuinely need to lock a specific physical unit at booking time (e.g. a boutique hotel assigning a room number up front rather than at check-in).

## Q zh
在酒店/民宿预订系统里，为什么通常优先选择'每个房型每晚一行，带总量和已订数量计数器'的模型，而不是 PostgreSQL 通过 `EXCLUDE USING GIST (during WITH &&)` 原生支持的'每个物理房间实例一行、用日期区间排他约束'的模型？

## A zh
按物理单元建的区间排他约束行，只能保证'同一个物理单元不出现两段重叠预订'——它无法表达'50 个可互换房间，总共最多卖 50 份'这种池化容量语义，除非建 50 个各自独立的约束行分别维护；而且它会在入住前就把客人绑定到一个具体物理单元，可能出现「某个特定单元被占、但等价的另一个单元还空着」却显示「已满」的假象。按房型-夜计数的行让任意一个可互换单元都能满足一次预订，装箱效率最大化；排他约束模型只留给那些确实需要在预订时就锁定具体物理单元（比如精品酒店在预订时而非入住时分配房间号）的场景。
