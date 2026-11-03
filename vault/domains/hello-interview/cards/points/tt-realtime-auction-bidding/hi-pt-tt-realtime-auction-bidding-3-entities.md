---
id: hi-pt-tt-realtime-auction-bidding-3-entities
node: tt.sd.tt-realtime-auction-bidding.points
type: qa
step: 3
---
## Q
**实时竞价拍卖 · Auction 与 Bid 的关键字段**｜必会 · 出自：实时竞价拍卖 › 核心实体与接口

`Auction` 和 `Bid` 的哪些字段支撑了排序、幂等和推送？

## A
**Auction。** 金额用整数分；`version` 每接受一次出价加 1，同时是「当前状态序号」，推送和重连都靠它。
**Bid。** `seq` 是拍卖内接受序号，`(auction_id, seq)` 唯一；`(auction_id, bidder_id, idempotency_key)` 唯一。
**订单。** 以 `auction_id` 为键，保证一场拍卖只产生一张订单。
