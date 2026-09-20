---
id: problems-restaurant-reservation-grace-lazy-sweep
node: problems.booking.restaurant
type: qa
step: 9
tags: [grown]
---
## Q
餐厅管理设计里，一次预订没人认领（客人没来也没取消），这张桌子的这个时段要怎么重新变得可订、可坐，为什么不用一个后台定时任务去扫描过期预订？

## A
`FloorManager` 给每次预订配一个宽限期：从预订时段开始算，宽限期内桌子替客人留着，`_smallest_free_fit` 和 `seat_from_waitlist` 都会跳过它；过了宽限期还没被认领，`_sweep` 就把这条预订从表里删掉——不删的话它会一直占着 `_overlaps` 的一个位置，这张桌子的这个时段以后谁都订不到。`_sweep` 不是由定时器驱动的，而是懒惰重算：`seat_walk_in`、`reserve`、`seat_reservation`、`clear_table`、`table`、`waitlist_length` 这些公开方法开头都会先调用它，把状态推到"此刻应该是什么样子"。好处是不用多养一个有自己生命周期、要处理并发写入的后台线程——没有人查询的时候，这条预订过期与否根本不重要。`_sweep` 清掉一条过期预订之后，还会在同一次加锁里顺手看一眼候位名单，把这张刚空出来的桌子给排在最前面、坐得下的那一位——这正是"候位名单有机会顶上"这句承诺的完整实现。
