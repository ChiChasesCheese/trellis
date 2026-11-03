---
id: hi-pt-tt-realtime-auction-bidding-8-version-reconnect
node: tt.sd.tt-realtime-auction-bidding.points
type: qa
step: 7
---
## Q
**实时竞价拍卖 · 版本号与断线重连**｜必会 · 出自：实时竞价拍卖 › 深入 3

推送乱序、重复，客户端断线重连后怎么追上状态？为什么不补发中间的每次出价？

## A
**版本。** 每条推送带 `version`，客户端丢弃不大于已展示版本的消息，乱序重复无害。
**重连。** 先 `GET /auctions/{id}` 拿当前快照和版本号，再订阅；价格是状态而不是事件流，不需补发。出价历史用快照里的最近几条加分页。
**其他。** 心跳检测断线；倒计时由客户端按结束时间戳本地算。
