---
id: hi-pt-tt-realtime-auction-bidding-6-idempotency
node: tt.sd.tt-realtime-auction-bidding.points
type: qa
step: 5
---
## Q
**实时竞价拍卖 · 出价幂等与同价并发**｜必会 · 出自：实时竞价拍卖 › 深入 2

手机超时重试同一出价，第一次其实已生效，第二次会被当「金额太低」拒绝，用户看到失败。怎么处理？同价并发谁赢？

## A
**幂等。** `(auction_id, bidder_id, idempotency_key)` 唯一约束，与出价同一事务插入；重复请求先按键查，查到就原样返回第一次结果，不再校验。键保存到拍卖结束后一段时间。
**同价。** 服务端分配的 `seq` 为准，先处理的成为最高价，后到者因未超过最高价加增幅被拒；不信客户端时间戳。
**代理出价。** 在拥有者内部处理，序号照常递增。
