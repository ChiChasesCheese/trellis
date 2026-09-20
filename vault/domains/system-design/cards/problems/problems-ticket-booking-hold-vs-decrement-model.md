---
id: problems-ticket-booking-hold-vs-decrement-model
node: problems.commerce.ticket-booking
type: qa
step: 4
tags: [grown]
---
## Q
Why doesn't the atomic-decrement inventory pattern used for general-admission flash sales (e.g. `UPDATE stock = stock - 1 WHERE stock > 0`) work for an assigned-seating ticket booking system?

## A
Atomic decrement treats inventory as a single number, which is correct for undifferentiated general-admission tickets but breaks down when tickets are distinct physical seats: a counter can tell you how many tickets are left but not which specific seat a buyer gets. Assigned seating needs a one-row-per-seat state machine (available/held/sold) so a buyer can pick and be assigned a specific seat, which is a fundamentally different concurrency problem — many distinct objects each claimed exactly once, not one shared count decremented many times.

## Q zh
为什么通用入场（general admission）闪购常用的原子递减库存模式（如 `UPDATE stock = stock - 1 WHERE stock > 0`）不适用于划位票务预订系统？

## A zh
原子递减把库存当成一个数字来处理，这对不区分座位的通用入场票是对的，但票如果是具体的物理座位就不成立了：计数器只能告诉你还剩多少张票，不能告诉你某个买家具体买到了哪个座位。划位场景需要"一票一行"的状态机（available/held/sold），让买家能选中并被分配到一个具体座位——这是本质不同的并发问题：是很多个不同对象各自被恰好认领一次，而不是一个共享计数被反复递减。
