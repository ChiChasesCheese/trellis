---
id: hi-pt-crowdfunding-share-purchase-3-atomic-reserve
node: qb.sd.crowdfunding-share-purchase.points
type: qa
step: 3
---
## Q
**限时众筹购股系统 · 原子扣库存**｜必会 · 出自：限时众筹购股系统 › 整体设计

众筹购股开抢后，大量请求同时扣减同一个全局剩余股数。怎样保证绝不超卖？

## A
**要点。** 在 Redis 里用一段 Lua 脚本原子地"剩余 ≥ 请求股数则扣减并返回成功，否则返回售罄"，脚本在 Redis 中串行执行，所以不会超卖。
**状态。** 成功后购买行写成 RESERVED 并记过期时间（如 5 分钟）。售罄直接失败，不再碰余额服务。
**不变量。** 已确认股数 + 有效预留股数 ≤ 1,000 万。
