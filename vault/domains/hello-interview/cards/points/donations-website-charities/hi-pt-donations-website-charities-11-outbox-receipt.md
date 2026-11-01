---
id: hi-pt-donations-website-charities-11-outbox-receipt
node: qb.sd.donations-website-charities.points
type: qa
step: 11
---
## Q
**限时捐款网站 · 发件箱与回执**｜出自：限时捐款网站 › 整体设计

支付成功后要给用户发回执邮件。怎样避免状态已改但邮件事件丢失？邮件重复怎么办？

## A
**做法。** 在同一个数据库事务里写状态更新和一条发件箱（outbox）记录，发件箱投递器再推到队列，回执服务消费后发邮件。
**语义。** 邮件至少发一次，用 `donationId` 去重。
**失败。** 邮件经队列重试，退避加死信队列，不影响支付状态；用户在状态页可看到成功。
