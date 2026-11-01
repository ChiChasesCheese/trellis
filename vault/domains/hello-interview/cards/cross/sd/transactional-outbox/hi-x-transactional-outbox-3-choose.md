---
id: hi-x-transactional-outbox-3-choose
node: sd.cross.transactional-outbox
type: qa
step: 3
---
## Q
**事务外盒与可靠发布事件 (Transactional Outbox)**｜跨题模式 · 怎么选

面对一道新题，什么时候必须上 outbox？上了以后下游还要补什么？请按判断信号分支，各举一题。

## A
**先判断要不要：** 只要"改状态"和"通知别人"必须同生同灭，就要 outbox；如果下游事件丢了无所谓，就不要为它付这个成本。

1. **事件是第二半步，丢了账就不平**（跨分片转账、礼物收益入账）：必须 outbox，接收方用业务键幂等入账，失败有补偿。例：[[tt-wallet-ledger-service|钱包与复式账本服务]]、[[tt-live-gift-coin-settlement|直播虚拟礼物]]。
2. **下游是外部系统**（商户、交易所、供应商）：outbox 之后再加一层对外约束。商户加退避和按端点隔离；交易所加唯一引用号；供应商加幂等键和状态机恢复。例：[[tt-merchant-webhook-delivery|商户回调投递系统]]、[[stock-trading-platform|股票交易平台]]、[[hotel-booking-system|酒店预订系统]]。
3. **下游只是通知**：用最简单的 outbox 加去重即可，通知失败不改变业务结果。例：[[donations-website-charities|限时捐款网站]]。
4. **事件有轻重之分**：只给"丢了会出事"的那类走 outbox，其余尽力而为。例：[[tt-realtime-auction-bidding|实时竞价拍卖]]里被超越的通知可丢，赢家和付款消息走 outbox。
5. **事件量大且同一实体反复变**：outbox 之后接聚合器做合并削峰，按实体分区。例：[[food-item-reviews|带打赏的菜品评价系统]]。

**需要顺序**时，不要指望 outbox 本身有序，选一个实体键做分区键。
