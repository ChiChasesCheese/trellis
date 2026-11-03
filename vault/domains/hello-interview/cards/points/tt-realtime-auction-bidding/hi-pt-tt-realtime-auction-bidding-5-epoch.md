---
id: hi-pt-tt-realtime-auction-bidding-5-epoch
node: tt.sd.tt-realtime-auction-bidding.points
type: qa
step: 8
---
## Q
**实时竞价拍卖 · 拥有者租约与世代号**｜追问 · 出自：实时竞价拍卖 › 深入 4

拥有者因网络分区被判失联，新拥有者接手，旧拥有者仍有在途写入，怎么避免两个主？

## A
**做法。** 拥有关系靠租约加世代号 `epoch`；写入条件里带 `epoch`，数据库只接受当前世代，旧世代写入被拒。
**效果。** 即使两个人都认为自己是拥有者，也只有一个能成功。正确性靠约束，不靠「保证只有一个写者」。
