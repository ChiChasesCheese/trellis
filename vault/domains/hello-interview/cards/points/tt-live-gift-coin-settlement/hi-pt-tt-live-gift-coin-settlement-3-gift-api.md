---
id: hi-pt-tt-live-gift-coin-settlement-3-gift-api
node: tt.sd.tt-live-gift-coin-settlement.points
type: qa
step: 3
---
## Q
**直播礼物金币记账与主播结算 · 送礼接口与去重键**｜必会 · 出自：直播礼物金币记账与主播结算 › 核心实体与接口

送礼接口的请求、返回码和去重键怎么设计？价格和金额由谁决定、怎么存？

## A
**接口。** `POST /v1/gifts {gift_id, room_id, gift_type, count}`：200 返回新余额，402 余额不足，409 同一个 gift_id 内容不同。
**去重键。** gift_id 由客户端点击时生成，重试复用；充值用 `(platform, transaction_id)` 做主键。
**细节。** 价格由服务端按当时价格版本决定，忽略客户端价格；金额全是整数，分成用 `share_micro`（万分之一金币）。
