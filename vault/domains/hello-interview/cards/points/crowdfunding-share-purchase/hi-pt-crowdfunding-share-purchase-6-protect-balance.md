---
id: hi-pt-crowdfunding-share-purchase-6-protect-balance
node: qb.sd.crowdfunding-share-purchase.points
type: qa
step: 6
---
## Q
**限时众筹购股系统 · 保护余额服务**｜出自：限时众筹购股系统 › 深入 3

余额服务承载全公司的资金业务，众筹购股活动不能把它冲垮。有哪些具体手段？

## A
**限流。** 等候室加入口限流，把调用速率压到约定值（如 2,000 次/秒）；500 万人 1 小时平均只需约 1,400 次/秒，余量足够。
**少调用。** 不先 lookupBalance 再扣款（有时间窗口且多一次调用），直接 withdraw，余额不足由它拒绝；lookupBalance 只用于页面展示并缓存。
**降级。** 熔断加退避，变慢时快速失败，避免重试风暴；单用户串行。
