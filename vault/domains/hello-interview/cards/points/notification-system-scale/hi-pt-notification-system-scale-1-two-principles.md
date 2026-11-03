---
id: hi-pt-notification-system-scale-1-two-principles
node: qb.sd.notification-system-scale.points
type: qa
step: 1
---
## Q
**百万级通知系统 · 两条第一原则**｜必会 · 出自：百万级通知系统 › 需求

设计支持单发与群发、峰值每秒百万条的通知系统，关键通知（验证码、聊天）和促销共用管道会出什么问题？总的设计原则是什么？

## A
**问题。** 促销洪峰会把验证码和聊天提醒压在队列后面。
**原则一。** 按优先级物理隔离。
**原则二。** 群发在系统内部懒扇出，并且每条消息都带过期时间，真正发送前再检查一次。
