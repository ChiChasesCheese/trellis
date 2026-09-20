---
id: problems-flash-sale-reservation-ttl-vs-ticket-booking
node: problems.commerce.flash-sale
type: qa
step: 6
tags: [grown]
---
## Q
A flash sale gives a successful buyer a 3-minute reservation window to complete payment before the unit is released back to the pool, noticeably shorter than the roughly 10-minute seat hold used by an assigned-seating ticket booking system. Why is a shorter window appropriate here?

## A
A ticket booking system's longer hold accommodates a buyer filling out payment details for the first time; a flash sale's buyers have typically already saved a default payment method on the platform, so the reservation mainly needs to cover payment-gateway confirmation time, not manual form-filling. Combined with the fact that a flash sale's queue behind the reservation holder is often tens of times larger than the remaining stock, the faster turnaround from a shorter TTL lets more waiting buyers get a chance within the sale's brief window — the benefit of quick recycling outweighs the benefit of a generous window in this specific supply-to-demand ratio.

## Q zh
秒杀给成功抢到名额的买家一个 3 分钟的保留窗口去完成支付，明显短于划位票务预订系统约 10 分钟的座位占用时长。为什么这里适合用更短的窗口？

## A zh
票务预订系统的更长占用是为了容纳买家第一次现场填写支付信息；秒杀的买家通常已经在平台上绑定了默认支付方式，保留窗口主要只需要覆盖支付网关确认扣款的时间，而不是手动填表的时间。再加上秒杀场景里排在保留名额后面的等待队列往往是剩余库存的几十倍，更短 TTL 带来的更快周转能让更多在等待的买家在这场短暂的秒杀窗口内获得机会——在这种供需比下，快速回收的收益大于给一个宽松窗口的收益。
