---
nodes: [problems.booking.hotel-booking]
url: https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/hotel-management-system.md
---
# awesome-low-level-design — Hotel Management System

值得读：流传最广的参照系，同一份设计用六种语言（含 Python）并排给出，可以用来对照自己有没有
漏掉需求面（房型、预订、入住退房、支付、并发）。它把库存建成 `Room.status`（AVAILABLE /
BOOKED / OCCUPIED）加一张 `Reservation` 列表，也就是"每间房一条时间线"那条路；总控类是
Singleton，并发靠 synchronized 方法。本题解在三点上明确反着做：库存单位是"房型 × 一晚"的计数
而不是房间状态（一个房间状态字段没法表达"下周二这间房已经被订了"）、房号到入住才绑定、拒绝
Singleton。它的支付方式抽象在本题解里被整块省掉，因为那属于另一道题。
