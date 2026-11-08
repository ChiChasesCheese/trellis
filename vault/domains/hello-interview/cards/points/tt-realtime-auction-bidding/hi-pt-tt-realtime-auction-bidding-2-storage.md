---
id: hi-pt-tt-realtime-auction-bidding-2-storage
node: tt.sd.tt-realtime-auction-bidding.points
type: qa
step: 2
---
## Q
**实时竞价拍卖 · 存储估算**｜必会 · 出自：实时竞价拍卖 › 需求

单场热门拍卖每秒 1000 次出价、每条约 200 字节，存储是瓶颈吗？

## A
**数字。** 按全天都保持这个速率的上限估算，每天 8640 万条，约 17 GB；一年约 6 TB，普通分库分表可承受。
**要点。** 只有被接受的出价才写入，被拒绝的只记日志；真正的上限是数据库写入，不是容量。
