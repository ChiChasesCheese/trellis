---
id: hi-pt-hotel-booking-system-9-stale-verify
node: qb.sd.hotel-booking-system.points
type: qa
step: 9
---
## Q
**酒店预订系统 · 过期搜索与下单核验**｜追问 · 出自：酒店预订系统 › 深入 6

搜索结果可能是过期的。用户看到的价格和可订性怎么保证最终准确？

## A
**要点。** 搜索结果带 `as_of` 时间；用户点进详情和下单时再向实时库存（或供应商）核验价格和可订性，价格变化要明确提示。
**为什么。** 预聚合牺牲几十秒新鲜度，换读的两个数量级降幅。
