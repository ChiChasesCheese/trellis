---
nodes: [problems.booking.airline]
url: https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/airline-management-system.md
tags: []
---
# Designing an Airline Management System

值得读：流传最广的参照系，Python/Java/C++/C#/Go 五语言并排实现。`Flight.available_seats` 是
一张座位列表、`Seat.status` 直接记状态枚举，没有日期维度，无法表达"同一航线不同日期库存不同"；
`BookingManager`/`PaymentProcessor` 用 `__new__` 双重检查锁写成 Singleton；不建 `Itinerary`、
不判中转与最短衔接时间、不做超售。本文与它的分歧点集中在「关键设计决策」与「常见错误」两节。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/airline-management-system.md)
%% trellis:end %%
