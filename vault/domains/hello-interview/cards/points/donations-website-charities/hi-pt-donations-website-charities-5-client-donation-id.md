---
id: hi-pt-donations-website-charities-5-client-donation-id
node: qb.sd.donations-website-charities.points
type: qa
step: 5
---
## Q
**限时捐款网站 · 前端生成 donationId**｜出自：限时捐款网站 › 整体设计

捐款请求的幂等键 `donationId` 应该由前端生成还是服务端生成？它如何同时保护我们自己的库和 PSP？

## A
**要点。** 页面加载时由前端生成 UUID 随表单提交。用户连点、网络重发、后退重交都是同一个 ID，数据库唯一约束保证只有一条记录。
**为什么。** 服务端生成的 ID 在用户重发时无法关联；客户端生成让同一次意图在任何重试中保持同一个键。
**PSP。** `donationId` 同时作为 PSP 的幂等键（idempotency key）。
