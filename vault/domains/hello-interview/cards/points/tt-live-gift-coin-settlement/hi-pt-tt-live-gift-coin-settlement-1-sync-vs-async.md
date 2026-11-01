---
id: hi-pt-tt-live-gift-coin-settlement-1-sync-vs-async
node: tt.sd.tt-live-gift-coin-settlement.points
type: qa
step: 1
---
## Q
**直播礼物金币记账与主播结算 · 同步的钱与异步的账**｜出自：直播礼物金币记账与主播结算 › 需求

直播礼物系统里观众钱包和主播收益的一致性要求有什么不同？核心设计原则是什么？

## A
**要点。** 观众的钱包必须强一致、恰好一次地扣币；主播这一侧的收益只是事件的汇总。
**原则。** 把同步的钱和异步的账分开：实时展示可以是估计值，周结算能由事件重算并对上每一分钱。
