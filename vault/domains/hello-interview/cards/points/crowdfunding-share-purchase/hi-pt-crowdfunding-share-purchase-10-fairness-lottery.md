---
id: hi-pt-crowdfunding-share-purchase-10-fairness-lottery
node: qb.sd.crowdfunding-share-purchase.points
type: qa
step: 10
---
## Q
**限时众筹购股系统 · 供大于求的公平性**｜加分 · 出自：限时众筹购股系统 › 取舍与追问

众筹购股需求远大于供给，先到先得对网络快的人有利。有什么替代方案，代价是什么？

## A
**方案。** 改为抽签：窗口内收集意向并先冻结资金，窗口结束后随机分配，未中者退款。
**好处。** 没有抢的并发问题。
**代价。** 流程更长，资金冻结时间更久。
**相关。** 单人限购在库里按 (eventId, userId) 汇总已购股数，用条件更新保证不超上限。
