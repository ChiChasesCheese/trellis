---
id: hi-pt-tt-live-gift-coin-settlement-11-refund-redis
node: tt.sd.tt-live-gift-coin-settlement.points
type: qa
step: 11
---
## Q
**直播礼物金币记账与主播结算 · 退款与为何不用 Redis 记余额**｜追问 · 出自：直播礼物金币记账与主播结算 › 取舍与追问

应用商店在币花光后才发来退款通知怎么办？为什么不用 Redis 记余额？

## A
**退款。** 写负的冲销流水，余额可为负，钱包进入负债状态并禁止送礼；主播收益设保留期（如 7 天），期内币被追回则对应收益冲销，期外由平台承担坏账。这是产品和风控取舍，要明说。
**Redis。** 主从异步复制，故障转移丢最近扣减，用户平白多出币；Redis 只能缓存读取，扣减落在有同步副本的关系库。
