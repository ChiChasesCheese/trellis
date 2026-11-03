---
id: hi-pt-donations-website-charities-6-triple-idempotency
node: qb.sd.donations-website-charities.points
type: qa
step: 6
---
## Q
**限时捐款网站 · 防重复扣款的三层防护**｜必会 · 出自：限时捐款网站 › 深入 1

重复扣款可能来自用户重复提交、我们的重试和 PSP 的超时。服务端和 PSP 各用什么机制防护？前端按钮置灰算保证吗？

## A
**前端。** 提交后按钮置灰只是体验，不是保证。
**服务端。** `donationId` 唯一约束加状态机；只有 `CREATED → PROCESSING` 的转换能触发 PSP 调用，用条件更新 `WHERE status='CREATED'`，并发下只有一个请求赢。
**PSP。** 同一个幂等键，PSP 保证只处理一次并返回同样结果。
**易错。** 三层叠加，缺一个都可能出事故。
