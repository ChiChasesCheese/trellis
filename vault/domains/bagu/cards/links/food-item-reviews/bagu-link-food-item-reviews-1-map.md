---
id: bagu-link-food-item-reviews-1-map
node: links.food-item-reviews
type: qa
step: 1
---
## Q
**带打赏的菜品评价系统（点评 + 投票 + 达标付款） · 会被追问哪些八股**｜必会

设计带打赏的菜品评价系统（点评 + 投票 + 达标付款）时，面试官最可能从哪几步下钻到基础知识？每一步问什么，怎么答？

## A
**基本回答。** 票是高频可刷的写入，钱是低频必须恰好付一次。基础是：幂等键与唯一约束、原子计数、缓存 Hash、行锁热点、里程碑号做付款幂等、金额整数。

**下钻路线。**
- 打赏连点 → 幂等键加唯一约束，[[a.idem.idempotency-design|幂等是什么、怎么实现]]
- 同一用户一票 → Set 判重加原子计数，数据库唯一索引兜底，[[a.scenario.like-leaderboard|点赞计数与实时排行榜]]
- 投票数和打赏金额放缓存 → 一个点评一个 Hash，HINCRBY，[[b.redis.key-design|Redis Key 与缓存结构怎么设计]]
- 爆款评论每秒几百票 → 同一行排队加锁，改分片计数或批量合并写，[[b.mysql.lock-types|MySQL 锁分类]]
- 每 100 赞付 1 美元只付一次 → 里程碑号 k 作付款幂等键，[[a.idem.payment-idempotency|支付与扣款接口的幂等设计]]
- 计数和付款怎么解耦 → 达标事件走 outbox，[[a.idem.outbox|本地消息表 / Outbox 与最大努力通知]]
- 金额怎么存 → 最小单位整数，[[b.runtime.java-money-bigdecimal|金额计算]]

**业务场景。** 直播间打赏连点：每次点击带同一个业务单号，赞数达标后的付款以里程碑号去重，不会重复付给主播。
**系统设计。** [[links.tt-live-gift-coin-settlement|直播虚拟礼物：金币记账与主播结算]]：同样先扣钱再汇总收益，但那里是平台币；[[links.donations-website-charities|限时捐款网站]]：同样第三方付款的重复与超时，没有投票计数。
