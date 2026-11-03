---
id: hi-pt-tt-live-gift-coin-settlement-5-double-entry
node: tt.sd.tt-live-gift-coin-settlement.points
type: qa
step: 5
---
## Q
**直播礼物金币记账与主播结算 · 每份礼物的复式分录**｜必会 · 出自：直播礼物金币记账与主播结算 › 整体设计

7 个金币的礼物、主播分成 35%，复式分录怎么记？币在会计上是什么？

## A
**分录。** 70,000 micro：借 `user_coin_liability` 70,000；贷 `creator_earnings_payable` 24,500；贷 `platform_gift_revenue` 45,500。三行相加为 0。
**解释。** 币是平台的预付负债，花出去的那一刻才变成平台收入。
