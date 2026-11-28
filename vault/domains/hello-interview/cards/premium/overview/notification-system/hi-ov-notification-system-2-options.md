---
id: hi-ov-notification-system-2-options
node: sd.problem-breakdowns.notification-system
type: qa
step: 2
tags: [通览]
---
## Q
**通知系统 · 高层设计**｜通览

通知系统的高层设计怎么搭？每个功能需求走哪条路径？

## A
**组件。** API 网关、通知服务、数据库、cron、邮件、短信与推送服务商。

**每条路径。**
- **单发与定时：** 网关验 API Key 并限流，通知服务查联系方式，写 PENDING 行，调服务商，更新为 SENT 或 FAILED；定时的写成 SCHEDULED，每分钟的 cron 捞出，走同一条路。
- **活动：** 写一行活动并立即返回 202；cron 到点读一次人群成员快照，对每个收件人走单发的路径。
- **偏好：** 偏好是用户的属性，经偏好接口写入；每条通知调服务商前检查最新偏好，被拦截的记为 SUPPRESSED 并写原因。

**存储。** 通知、活动、偏好放 Postgres 即可，没有特殊要求。推送的设备令牌由移动端上报，存在我们这边。
