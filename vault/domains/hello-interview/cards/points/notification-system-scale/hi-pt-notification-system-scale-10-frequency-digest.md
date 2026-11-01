---
id: hi-pt-notification-system-scale-10-frequency-digest
node: qb.sd.notification-system-scale.points
type: qa
step: 10
---
## Q
**百万级通知系统 · 多业务轰炸与摘要**｜出自：百万级通知系统 › 取舍与追问

同一用户被多个业务方同时通知，通知系统怎么办？为什么不让业务方各自调用服务商？

## A
**理由。** 各自调用会重复建设、撞速率限制，用户被轰炸且没有统一频率上限和退订。
**做法。** 按用户做频率上限与聚合：促销每天最多 N 条，聊天按会话合并成"你有 3 条新消息"（digest）。
**时区。** 要按用户本地时间发，则群发按时区切分，游标按时区分段。
