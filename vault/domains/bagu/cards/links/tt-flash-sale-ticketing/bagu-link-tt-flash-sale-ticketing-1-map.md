---
id: bagu-link-tt-flash-sale-ticketing-1-map
node: links.tt-flash-sale-ticketing
type: qa
step: 1
---
## Q
**秒杀抢票（排队、限流、防超卖） · 会被追问哪些八股**｜必会

设计秒杀抢票（排队、限流、防超卖）时，面试官最可能从哪几步下钻到基础知识？每一步问什么，怎么答？

## A
**基本回答。** 五十万请求争一千张票，主线是逐层便宜地拒绝。基础集中在：当前读与行锁防超卖、RC 减少间隙锁死锁、Redis Lua 原子预扣、TCC 式预占与补偿，以及 BASE 下的最终收敛。

**下钻路线。**
- 扣库存先查后改 → UPDATE ... WHERE n > 0 是当前读，快照读会丢失更新，[[a.mysql.mvcc|MVCC]]
- 为什么改用 RC → 没有间隙锁、死锁更少，但要求 binlog 为 ROW，[[a.mysql.isolation-levels|四个事务隔离级别与 ACID]]
- 批量改订单状态整表被锁 → 条件没走索引就全表加锁，必须缩小范围，[[a.mysql.gap-deadlock|间隙锁、next-key 锁与死锁排查]]
- 库存扣减和一人一单怎么原子 → 一段 Lua 同时判库存、扣减、记用户，[[b.redis.tx-lua-pipeline|Redis 事务、Lua 脚本与 Pipeline]]
- 瞬时流量又不超卖 → 入口限流，Redis 预扣决定资格，数据库条件更新兜底，[[a.scenario.flash-sale|秒杀系统]]
- 开抢前统一设置过期 → 大量 key 同时过期占主线程，TTL 加随机，[[a.redis.expire-eviction|过期键删除与内存淘汰]]
- 百万人同一秒涌入 → 签名准入令牌，抽签或排队室按库存路径容量放行，客户端 429 退避，[[b.scenario.waiting-room|排队室与抽签准入]]
- 预占请求超时、回滚先到 → 空回滚与悬挂检查，库存不会多加，[[a.idem.tcc|TCC]]
- 预扣后建单失败 → 软状态，超时回补让状态最终收敛，[[a.distributed.cap-base|CAP 与 BASE]]

**业务场景。** 直播间限量一千件开抢，付款回调在占位到期后才到：票已释放而钱已收，票还在就恢复订单，不在就自动退款。
**系统设计。** [[links.ticketmaster|票务预订（Ticketmaster）]]：同样削峰，多了选座和十分钟占位；[[links.distributed-rate-limiter|分布式限流器（Rate Limiter）]]：准入层的限流机制，这里的阈值要和库存挂钩。
