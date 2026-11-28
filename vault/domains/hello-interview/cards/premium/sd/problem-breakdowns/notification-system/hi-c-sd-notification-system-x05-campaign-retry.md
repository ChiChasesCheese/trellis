---
id: hi-c-sd-notification-system-x05-campaign-retry
node: sd.problem-breakdowns.notification-system.exam
type: qa
step: 5
---
## Q
**通知系统 · 预测：活动创建请求超时后重试**｜考点 · 必会

营销系统 POST /campaigns 后网络超时，客户端重试。接口没有幂等键时，100 万用户会收到几条？加了幂等键之后呢？cron 在扇出中途崩溃重跑呢？

## A
- **没有幂等键：** 第一次请求其实已成功，重试又创建一个新活动，得到新的 `campaignId`，消息 ID 是 `campaignId:userId`，两批 ID 不同，下游无从识别，每人收到 2 条，共 200 万条。
- **有幂等键：** 重试带同一个幂等键，服务端返回已有活动（同一个 `campaignId`），不再创建；每条消息 ID 不变。
- **cron 中途崩溃重跑：** 重跑重新读快照，对每个用户生成 `campaignId:userId`，与第一次相同，已入队的会被下游去重丢弃，没入队的补发。前提是 ID 由确定性规则派生，而不是随机生成。
- **要点：** 去重的前提是"稳定 ID"，而稳定 ID 的源头是调用方的幂等键，缺任何一环都会让下游失效。
- **加分：** 快照要固定：重跑时人群成员可能已变化，应把快照（或快照版本）与活动绑定，否则两次扇出的人群不一致。
