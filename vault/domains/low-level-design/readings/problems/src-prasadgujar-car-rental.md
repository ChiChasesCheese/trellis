---
nodes: [problems.booking.car-rental]
url: https://github.com/prasadgujar/low-level-design-primer/blob/master/solutions.md
tags: [no-archive]
---
# low-level-design-primer — Object Oriented Design Solutions

值得读：一份面向对象设计题的索引式清单（仓库无 LICENSE 文件，只链接不摘录）。它把租车系统和
图书馆、停车场、酒店、电影订票归在同一类"预订与库存"之下，每题给需求要点、类清单和活动图的
方向，不给实现。用它做两件事最划算：确认这道题在面试里的标准问法，以及看清同类题被认为共享
哪些套路（目录、实体、预订、支付、通知）。

和本题解的分歧正好在它省略的那一半。它列的实体是 `Car` / `Customer` / `Reservation` /
`RentalSystem`，可用性被当成"查一下有没有冲突的预订"一句带过；而这道题真正的难点是**异地还车
（one-way）之下，可用性不再是一个只看时间的谓词**——车被上一段租约搬走了，所以"某门店那时候有没有
车"取决于车**将会**在哪。本题解把库存单位定成带 `origin` / `destination` 的一段行程，并把
"门店首尾相接 + 周转缓冲"写成唯一一条不变量；迟还挤占、事故封车、改派都复用这条判据，
这些在清单里都没有出现。
