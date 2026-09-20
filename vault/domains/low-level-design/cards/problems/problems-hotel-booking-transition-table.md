---
id: problems-hotel-booking-transition-table
node: problems.booking.hotel-booking
type: qa
step: 7
tags: [grown]
---
## Q
酒店订单有 RESERVED、CHECKED_IN、CHECKED_OUT、CANCELLED 四个状态。把合法转移写成一张 `状态 → 允许去往的状态集合` 的表，比在 `cancel`/`check_in`/`check_out` 各写一串 `if` 好在哪里？为什么不给每个状态建一个类？

## A
写成表的好处：新增一个状态（比如 NO_SHOW，到点没来）只要加一行和一条边，不用翻遍每一处状态判断；而且这张表本身就是可以直接贴给面试官看的状态图，一眼能看全。它还顺手解决一个并发问题——`cancel` 在锁内先调 `transition_to(CANCELLED)`，这一步就是"认领"订单：两个线程同时点取消只有一个能翻成功，另一个拿到非法转移异常，于是库存只会被还一次，幂等性建在状态机上而不是库存层的去重里。不建状态类，是因为状态模式（State）只在每个状态有一大段**各不相同的行为**时才划算；这里每条边的动作只有一两行，拆成四个类只会把一张表摊成四个文件。
