---
id: problems-hotel-reservation-cross-channel-conflict
node: problems.commerce.hotel-reservation
type: qa
step: 7
tags: [grown]
---
## Q
A hotel property sells the same physical rooms through both its own platform and an external OTA channel. When the platform and the external channel's webhook both try to confirm a booking for the same last-available night at nearly the same time, how should the system decide who wins, and what happens to the loser?

## A
The external channel's webhook is treated as just another writer competing for the same conditional UPDATE against the shared inventory table — whichever request's UPDATE reaches the database first and satisfies the capacity WHERE clause wins; the later one fails the same way a second internal booking attempt would. The losing side then enters a reconciliation flow rather than being silently dropped: if the platform's own confirmed booking loses (payment may already be collected), it triggers an automatic refund and apology flow; if an external channel's pushed event loses, the platform reports a conflict back to that channel to handle. Cross-channel sync is inherently eventually consistent because the two systems don't share a database transaction, so this reconciliation path is mandatory, not an edge case.

## Q zh
一家酒店同时在自己的平台和一个外部 OTA 渠道上出售同一批物理房间。当平台内部预订和外部渠道的 webhook 几乎同时争抢同一晚最后一间房的确认权时，系统该怎么判定谁赢？输的一方怎么处理？

## A zh
外部渠道的 webhook 被当成和平台内部预订完全一样的一个写入方，去争抢对同一张库存表的同一次条件更新——谁的 UPDATE 先到达数据库并满足容量的 WHERE 子句，谁就赢；后到的一方失败的方式和内部第二笔预订失败完全一样。输的一方会进入对账流程，而不是被静默丢弃：如果输的是平台自己已确认的预订（可能已经收款），触发自动退款和道歉流程；如果输的是外部渠道推来的事件，平台把冲突回报给该渠道自行处理。跨渠道同步天然是最终一致的，因为两个系统不共享同一个数据库事务，所以这条对账路径是必须存在的机制，不是一个可以忽略的边缘情况。
