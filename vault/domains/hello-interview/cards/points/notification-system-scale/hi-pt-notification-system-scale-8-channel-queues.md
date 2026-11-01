---
id: hi-pt-notification-system-scale-8-channel-queues
node: qb.sd.notification-system-scale.points
type: qa
step: 8
---
## Q
**百万级通知系统 · 渠道队列与回执**｜出自：百万级通知系统 › 整体设计

通知系统的处理流水线如何分层，为什么推送、短信、邮件各自一个队列？回执怎么用？

## A
**流水线。** 查偏好（本地缓存加 Redis）→ 查过期 → 渲染模板（内存缓存）→ 路由到渠道队列。
**为什么分队列。** 各通道速率限制和失败特征不同。
**回执。** 服务商回调更新 Delivery 状态；推送返回令牌无效时删除该设备令牌。
