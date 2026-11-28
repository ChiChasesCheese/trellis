---
id: bagu-link-tt-live-gift-coin-settlement-1-map
node: links.tt-live-gift-coin-settlement
type: qa
step: 1
---
## Q
**直播虚拟礼物：金币记账与主播结算 · 会被追问哪些八股**｜必会

设计直播虚拟礼物：金币记账与主播结算时，面试官最可能从哪几步下钻到基础知识？每一步问什么，怎么答？

## A
**基本回答。** 钱包扣币要强一致，主播收益只是事件的汇总，所以基础集中在：幂等键加条件扣币、发件箱加消费者去重、热点账户不做同步更新、扣币与展示分别选一致和可用，最后用对账验证。

**下钻路线。**
- 观众连点送礼 → gift_id 作主键，条件扣币 `coins >= 价格`，同一个本地事务，[[a.idem.payment-idempotency|支付与扣款接口的幂等设计]]
- 扣币后怎么通知主播侧 → 同事务写发件箱，至少一次投递，消费者按 gift_id 去重，[[a.idem.outbox|本地消息表 / Outbox 与最大努力通知]]
- 为什么不用 Redis 记余额 → 异步复制，切换会丢最近的扣减，Redis 只做缓存，[[a.redis.ha-overview|主从、哨兵与 Cluster 怎么保证高可用]]
- 热门主播每秒五千份 → 主播侧不做同步更新，只写事件，事件按 gift_id 而不是主播分区，账本只追加，余额等于快照加增量，[[b.scenario.ledger-design|复式账本]]
- 应用商店充值通知怎么验真 → 对时间戳加原始体做 HMAC，恒定时间比较，窗口外拒收，[[b.scenario.request-signing-keys|请求签名与密钥轮换]]
- 榜单和账务什么关系 → 账务是真相，榜单是可丢弃可重建的派生视图，[[a.scenario.like-leaderboard|点赞计数与实时排行榜]]
- 扣币和收益展示怎么取舍 → 扣币选一致，收益榜选可用加最终一致，[[a.distributed.cap-base|CAP 与 BASE]]
- 分成 35% 每份向下取整 → 累计系统性误差，用微单位整数，周期汇总才取整一次，[[b.runtime.java-money-bigdecimal|金额计算]]
- 周结算怎么证明对得上 → 币总量守恒与结算单等于事件汇总两条不变量，[[a.idem.selection-reconciliation|分布式事务选型、最终一致与对账]]

**业务场景。** 观众在网络抖动时连点三次「嘉年华」，客户端重试复用同一个 gift_id，只扣一次币；应用商店充值通知重复到达，同样靠主键吸收。
**系统设计。** [[links.payment-batch-processing|支付处理系统（授权冻结 + 每日批量结算）]]：同样靠幂等和对账，但那里有外部渠道的超时未知，这里币是平台内部的预付负债；[[links.realtime-game-leaderboard|在线游戏排行榜（全球榜 + 我的名次 + 好友榜）]]：礼物榜就是它，只是展示，不能当账。
