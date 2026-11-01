---
id: hi-pt-donations-website-charities-4-donation-state
node: qb.sd.donations-website-charities.points
type: qa
step: 4
---
## Q
**限时捐款网站 · 捐款状态机**｜出自：限时捐款网站 › 核心实体与接口

捐款记录的状态机应该包含哪些状态？PSP 超时时记成什么？这个状态怎么收敛？

## A
**状态。** `CREATED → PROCESSING → SUCCEEDED | FAILED | UNKNOWN`。
**UNKNOWN。** 超时或 5xx 时进入，表示结果未知；经对账任务变成 SUCCEEDED 或 FAILED。
**做法。** 明确拒绝（余额不足、卡被拒、风控拦截）直接记 FAILED 并提示用户换卡；UNKNOWN 不能让用户直接重试，否则可能扣两次。
