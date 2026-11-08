---
id: hi-x-transactional-outbox-2-compare
node: sd.cross.transactional-outbox
type: qa
step: 2
---
## Q
**事务外盒与可靠发布事件 (Transactional Outbox)**｜跨题模式 · 对比

八道题都用了事务外盒，但投递的对象和消费端的约束不同。请按题说明 outbox 在里面送给谁，以及为什么每道题的重点不一样。

## A
| 题 | 在这里怎么用 | 为什么和别的题不同 |
|---|---|---|
| [[tt-merchant-webhook-delivery\|商户回调投递系统]] | 支付服务在更新状态的同一事务里写 Event，再扇出到各商户的投递表 | 下游是外部商户：后面还要指数退避、按端点隔离的并发额度、商户按事件号去重；积压放存储不放队列 |
| [[tt-live-gift-coin-settlement\|直播虚拟礼物：金币记账与主播结算]] | 扣币事务同时写事件、币流水和 outbox，中继把事件投给收益聚合器 | 发件箱只保证至少一次，所以聚合器必须按 `gift_id` 去重；收益走异步，不碰同步扣币路径 |
| [[tt-wallet-ledger-service\|钱包与复式账本服务]] | 每笔业务在本分片一个事务里写分录和 outbox；跨分片转账靠 outbox 把事件送到对方分片 | outbox 承担了转账的"第二半步"，接收方分片用同一个 `transfer_id` 幂等入账，失败还要走补偿 |
| [[tt-realtime-auction-bidding\|实时竞价拍卖]] | 出价和"出价已接受"事件同事务写 outbox，再投到按 `auction_id` 分区的 Kafka | 按重要性分级：被超越的通知可以丢，只有赢家和付款相关消息才必须经 outbox 保证送达 |
| [[stock-trading-platform\|股票交易平台]] | 冻结资金、写订单、写 outbox 在同一事务，进程在发出前崩溃，重启后继续发 | 投递对象是交易所下单，必须配唯一引用号（ClOrdID），否则重发会重复下单 |
| [[hotel-booking-system\|酒店预订系统]] | 状态变更和"调用供应商"的消息一起写 outbox，由中继投递 | 对应外部供应商的确认调用，要与状态机（PAID→PENDING_SUPPLIER→CONFIRMED）结合做恢复 |
| [[donations-website-charities\|限时捐款网站]] | 支付成功的状态更新与 outbox 同事务，投递器异步触发回执邮件 | 下游只是通知，失败不影响捐款结果，只需要最简单的至少一次，用 `donationId` 去重 |
| [[food-item-reviews\|带打赏的菜品评价系统]] | 票的差值经 outbox 写入事件流，聚合器按 `reviewId` 分区批量更新计数 | outbox 还兼削峰：热点评论一秒内的多次投票合并成一次更新 |

**共同点：** 本地事务里同时写业务行和事件行。**差异来自下游：** 外部商户要隔离，对方分片要幂等入账，交易所要引用号，通知可以降级，计数要合并。
