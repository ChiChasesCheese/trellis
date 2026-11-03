---
id: hi-pt-job-board-platform-9-notification
node: qb.lld.job-board-platform.points
type: qa
step: 6
---
## Q
**招聘信息平台 · 通知解耦**｜追问 · 出自：招聘信息平台 › 逐步扩展 2

招聘平台新申请要通知雇主、状态变化要通知求职者，渠道有邮件、站内信、推送。怎么设计才不影响核心流程？

## A
**要点。** 观察者模式：事件总线让各渠道自行订阅，主流程只发布事件。
**生产化。** 订阅者通过消息队列异步消费，对重复事件幂等；通知失败不能影响投递结果。
**为什么。** 新增渠道只加订阅者，不改 apply 和 update_status。
