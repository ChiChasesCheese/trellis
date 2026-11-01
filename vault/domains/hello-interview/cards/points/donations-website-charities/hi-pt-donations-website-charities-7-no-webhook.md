---
id: hi-pt-donations-website-charities-7-no-webhook
node: qb.sd.donations-website-charities.points
type: qa
step: 7
---
## Q
**限时捐款网站 · 不能用 webhook 时拿异步结果**｜出自：限时捐款网站 › 深入 2

面试官限制不允许使用 webhook。怎样拿到支付的最终结果？如果允许 webhook，它在设计里应该扮演什么角色？

## A
**同步确认。** 用 PSP 的服务端直接确认接口，响应里就带最终结果（卡支付通常即时）。需要 3-D Secure 等额外验证的支付，由前端完成验证后再调我们的确认接口。
**兜底。** 对账轮询：每隔几十秒扫描卡在 PROCESSING 或 UNKNOWN 的捐款，向 PSP 查真实结果，查到成功补成 SUCCEEDED 并触发回执，查不到则置 FAILED 允许重试。
**webhook。** 只当加速通知，因为它会丢、会重复、会乱序。
