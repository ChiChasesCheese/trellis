---
id: bagu-link-ticketmaster-1-map
node: links.ticketmaster
type: qa
step: 1
---
## Q
**票务预订（Ticketmaster） · 会被追问哪些八股**｜必会

设计票务预订（Ticketmaster）时，面试官最可能从哪几步下钻到基础知识？每一步问什么，怎么答？

## A
**基本回答。** 难在开票洪峰、座位不能重复卖、占座到期释放，以及锁座、支付、出票跨服务一致。基础是：限流排队、缓存击穿防护、占座锁加唯一约束、条件更新、Saga 补偿。

**下钻路线。**
- 热门演出开票瞬间 → 入口限流加排队室，签名令牌按速率放行，系统扛不住时优雅排队，[[b.scenario.waiting-room|排队室与抽签准入]]
- 开票瞬间详情页缓存过期 → 互斥重建或逻辑过期，库只承受一次回源，[[b.cache.breakdown|缓存击穿]]
- 选座后占用十分钟 → `SET seat:id 用户 NX PX 600000`，确认和释放校验 value，[[a.distributed.lock-redis-setnx|用 Redis 实现分布式锁]]
- 同一座位不被订两次 → 唯一约束，RR 下间隙锁防插入，[[a.mysql.gap-deadlock|间隙锁、next-key 锁与死锁排查]]
- 一次锁多个座位 → 按座位号排序加锁，避免互相等待，[[b.runtime.java-deadlock-threads|线程基础与死锁]]
- 锁座后未支付怎么释放 → 延迟消息到期触发，[[b.scenario.delayed-task|定时调度与订单超时自动取消]]
- 占座到期与支付成功同时发生 → 条件更新决定谁赢，钱已收座位已放走退款，[[a.scenario.payment-system|支付系统设计]]
- 锁座、支付、出票三个服务 → Saga，出票失败补偿退款，退款幂等可重试，[[b.idem.saga|SAGA]]

**业务场景。** 座位保留十分钟，到期那一刻付款回调才到：座位已释放而钱已收，票还在就恢复订单，不在就自动退款。
**系统设计。** [[links.tt-flash-sale-ticketing|秒杀抢票（排队、限流、防超卖）]]：同样先削峰，不选座，库存是计数；[[links.online-auction|在线拍卖（eBay）]]：同样争用热点行，但比的是更高的价格。
