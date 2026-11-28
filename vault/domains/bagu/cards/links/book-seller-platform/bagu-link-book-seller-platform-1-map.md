---
id: bagu-link-book-seller-platform-1-map
node: links.book-seller-platform
type: qa
step: 1
---
## Q
**图书比价代购平台（Book Seller Platform） · 会被追问哪些八股**｜必会

设计图书比价代购平台（Book Seller Platform）时，面试官最可能从哪几步下钻到基础知识？每一步问什么，怎么答？

## A
**基本回答。** 对一堆不可靠的第三方扇出，并恰好成交一次。基础是：并发编排与整体超时、熔断隔离慢书商、下单幂等、超时未知、Saga 与 outbox、对账。

**下钻路线。**
- 并发请求多家书商 → CompletableFuture 编排，allOf 加整体超时；一家抛异常用其余结果，[[b.runtime.java-aqs-juc|AQS 与并发工具类]]
- 每家单独超时 → 整体 deadline 逐层递减，用已返回的结果，[[b.protect.timeout|超时时间怎么设置]]
- 一家书商变慢 → 对它熔断，半开状态用少量请求探测，[[b.protect.breaker|熔断器的三态与触发条件]]
- 用户重复点下单 → 幂等键，同键返回第一次的结果，[[a.idem.idempotency-design|幂等是什么、怎么实现]]
- 向书商下单超时 → 状态记未知，先查询，不换书商重下，[[a.idem.timeout-unknown|调用扣款接口超时了，到底扣了没有]]
- 支付、占书、通知多步骤 → Saga，失败走补偿并幂等，[[b.idem.saga|SAGA]]
- 订单已写入但消息没发出 → 同事务写 outbox，转发进程投递，[[a.idem.outbox|本地消息表 / Outbox 与最大努力通知]]
- 订单与库存分属两服务，重复乱序消息 → 状态机加对账，[[a.idem.selection-reconciliation|分布式事务选型、最终一致与对账]]

**业务场景。** 代购向书商扣款超时，不知道成交没有：必须先查询，直接换一家重下可能同一种书买两次。
**系统设计。** [[links.payment-batch-processing|支付处理系统（授权冻结 + 每日批量结算）]]：超时未知的处理同理，对象是支付渠道；[[links.hotel-booking-system|酒店预订系统（Expedia 型聚合与自营）]]：同样对多个供应商扇出并设超时，多了库存保留。
