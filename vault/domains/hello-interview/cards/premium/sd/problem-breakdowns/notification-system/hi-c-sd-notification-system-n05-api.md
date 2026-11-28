---
id: hi-c-sd-notification-system-n05-api
node: sd.problem-breakdowns.notification-system.notes
type: qa
step: 5
---
## Q
**通知系统 · 接口设计与状态码**｜摘要 · 必会

通知系统的发送、活动、偏好接口怎么设计？为什么活动要单独一个端点，返回 202 而不是 200？用户标识为什么出现在路径里？

## A
- **单发：** `POST /notifications`，体含 `userId`、`channel`（push、email、sms）、`priority`（high、standard）、`content`、可选 `scheduledAt`（默认现在）。起步假设同步调用服务商，所以返回 200 加状态；等投递移出请求路径，"接受"和"送达"就不是同一件事，要改成 202。
- **活动：** `POST /campaigns`，体含 `segmentId`、渠道、优先级、`templateId`、可选 `scheduledAt`，立即返回 202 和 id。单独端点是因为让一个端点有时创建通知、有时创建活动会语义混杂；202 是因为发送发生在以后，创建时没有结果可报。
- **偏好：** `PUT /users/{userId}/preferences`，体含 `optOuts` 与 `quietHours`（起止时间和时区）。偏好是对已知资源的整体替换，用 PUT 天然幂等。
- **设备令牌：** `PUT /users/{userId}/devices`，带平台和推送令牌。令牌会轮换，没有稳定来源可以同步，所以移动端在登录和变化时自己上报。
- **用户标识放路径：** 通常用户身份来自 JWT，由客户端传是警告信号；但这里调用方是用 API Key 认证的内部服务，替已认证的用户操作，所以放路径合理。平台团队可能追问授权如何传递，常见答案是委托令牌（delegation token）或服务账号。
- **后续：** 两个创建接口都会增加幂等键；先给简单契约再演进，并告诉面试官即可。
