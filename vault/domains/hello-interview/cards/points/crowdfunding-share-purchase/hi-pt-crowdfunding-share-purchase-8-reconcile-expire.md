---
id: hi-pt-crowdfunding-share-purchase-8-reconcile-expire
node: qb.sd.crowdfunding-share-purchase.points
type: qa
step: 7
---
## Q
**限时众筹购股系统 · 对账与预留过期**｜追问 · 出自：限时众筹购股系统 › 深入 4

众筹购股里有些购买卡在 RESERVED 或 PAYING，Redis 里的剩余数也可能和实际不一致。系统靠什么兜底？

## A
**要点。** 周期运行的对账与过期任务：找出超时的 RESERVED/PAYING，先核实余额服务的实际结果，再决定确认或回收股数。
**核对公式。** Redis 剩余数应等于 总数 − (已确认 + 有效预留)，不一致以数据库为准纠正。
**重建。** Redis 宕机后先从数据库重算再开放，期间短暂拒绝，比带着错误计数放行安全。
