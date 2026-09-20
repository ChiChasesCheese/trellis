---
id: problems-auction-contention-differs-from-ticket-booking
node: problems.commerce.auction
type: qa
step: 1
tags: [grown]
---
## Q
In an online auction, all bidders on one popular item compete to update the exact same row (the current highest bid). Why does this make a single-row conditional-write pattern (like `UPDATE ... WHERE version = :expected`, which works well for reserving one of many independent seats in a ticket-booking system) behave differently here than it does when many buyers are each trying to claim a different seat?

## A
In a ticket-booking system, contention is spread across many independent rows — ten thousand buyers usually aren't all fighting over the same seat, so most conditional writes succeed on the first try. In an auction, every bidder on a hot item is writing to the same single row, so the contention doesn't dilute across rows at all — it concentrates entirely on one row, and the fraction of conditional writes that lose the race and must retry rises sharply as bid arrival rate increases, which is exactly the scenario a per-item serialized writer is built to avoid.

## Q zh
在一场在线拍卖里，所有对同一件热门商品出价的人都在竞争更新完全相同的一行数据（当前最高价）。为什么这会让单行条件写模式（例如 `UPDATE ... WHERE version = :expected`，在票务预订系统里用来抢多个互相独立的座位之一时效果很好）在这里表现出不同的行为？

## A zh
在票务预订系统里，竞争分散在许多相互独立的行上——一万个买家通常不会全都抢同一个座位，所以大多数条件写第一次尝试就能成功。而在拍卖里，一件热门商品的每个出价者都在写同一行，竞争完全不会被分摊到多行上——而是全部集中在一行上，随着出价到达速率上升，条件写输掉竞争、需要重试的比例会急剧上升，这正是按商品分配单一序列化写者要避免的场景。
