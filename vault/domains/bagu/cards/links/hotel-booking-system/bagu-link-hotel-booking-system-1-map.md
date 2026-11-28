---
id: bagu-link-hotel-booking-system-1-map
node: links.hotel-booking-system
type: qa
step: 1
---
## Q
**酒店预订系统（Expedia 型聚合与自营） · 会被追问哪些八股**｜必会

设计酒店预订系统（Expedia 型聚合与自营）时，面试官最可能从哪几步下钻到基础知识？每一步问什么，怎么答？

## A
**基本回答。** 读极多、写极少，但写绝不能超卖。基础是：唯一约束与行锁防重复、热点房型的原子条件扣减、搜索与房态的 CDC 同步、多供应商超时、延迟释放保留。

**下钻路线。**
- 同一间房同一晚不被两人订走 → (room_id, 日期) 唯一约束，或对库存行 FOR UPDATE，[[b.mysql.phantom-read|幻读与 RR 下怎么解决]]
- 热门房型上千人下单 → 锁吞吐受持锁时间限制，分段或原子条件扣减，[[a.distributed.lock-redis-setnx|用 Redis 实现分布式锁]]
- 搜索走 ES，房态不一致 → CDC 异步同步，下单前回源校验，[[b.search.mysql-es-sync|MySQL 到 ES 的数据同步]]
- 并发查多个供应商 → 每家单独超时，整体 deadline 逐层递减，[[b.protect.timeout|超时时间怎么设置]]
- 订单与房量两个服务一致 → 状态机加消息驱动，重试幂等，定时对账，[[a.distributed.cap-base|CAP 与 BASE]]
- 保留库存的 TTL → 到期自动释放，支付成功要与释放竞争，[[b.scenario.delayed-task|定时调度与订单超时自动取消]]
- 外部依赖不可用 → Saga 状态机，不用两阶段提交，[[b.idem.saga|SAGA]]

**业务场景。** 抖音本地生活的酒店团购在节假日被抢订：保留到期时刻付款回调才到，房已释放而钱已收，要走退款。
**系统设计。** [[links.ticketmaster|票务预订（Ticketmaster）]]：同样限时保留加支付竞争，座位是单个实体而房型是计数；[[links.book-seller-platform|图书比价代购平台（Book Seller Platform）]]：同样对多个供应商扇出，没有库存保留。
