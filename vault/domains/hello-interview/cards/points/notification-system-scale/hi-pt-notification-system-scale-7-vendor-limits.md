---
id: hi-pt-notification-system-scale-7-vendor-limits
node: qb.sd.notification-system-scale.points
type: qa
step: 7
---
## Q
**百万级通知系统 · 第三方限速与故障**｜出自：百万级通知系统 › 深入 5

通知系统依赖 APNs、FCM、短信与邮件服务商，它们有速率限制也会故障。网关怎么应对？

## A
**限速。** 网关内用令牌桶按服务商限速，积压回压到渠道队列而不是丢弃。
**熔断。** 连续失败率超阈值打开熔断，流量切备用服务商，半开用少量探测流量恢复。
**批量。** FCM 一次可提交最多 500 个令牌；邮件按模板批量提交。
