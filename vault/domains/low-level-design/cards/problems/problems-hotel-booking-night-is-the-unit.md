---
id: problems-hotel-booking-night-is-the-unit
node: problems.booking.hotel-booking
type: qa
step: 1
tags: [grown]
---
## Q
在酒店预订（Hotel Booking）设计里，库存的计量单位该是"一间房"、"一天"，还是别的？6 月 1 日入住、6 月 3 日退房占用了几个单位？

## A
单位是**一个房型的一晚**。一次入住消耗的既不是一间房（同一间房在这段日期之前和之后照样能卖给别人），也不是一天（3 日上午退房的人和当天下午入住的人不冲突），而是这个房型在某几晚被占用。6 月 1 日入住、6 月 3 日退房是住 **2 晚**（1 号晚和 2 号晚），也就是半开区间 `[check_in, check_out)`。定成"晚"之后三件事同时变简单：退房当天自然不占用，不需要任何 `-1` 补丁；判两段入住冲突退化成 `a.check_in < b.check_out and b.check_in < a.check_out` 一行；可订量变成每晚一个整数计数，加减可以在一把锁里原子完成。
