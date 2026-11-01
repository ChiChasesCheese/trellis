---
id: hi-pt-donations-website-charities-1-core-difficulty
node: qb.sd.donations-website-charities.points
type: qa
step: 1
---
## Q
**限时捐款网站 · 难点在与第三方支付打交道的不确定性**｜出自：限时捐款网站 › 需求

设计一个只运行 24 到 72 小时、预先写死几家慈善机构、支付走第三方支付服务商（PSP）的捐款网站。业务本身极简单，真正的难点是什么？必须保证什么？

## A
**要点。** 难点全在和 PSP 打交道时的不确定性：用户点了两次、PSP 超时、PSP 挂了、webhook 丢了。
**保证。** 每种情况下都要做到"最多扣一次钱，且系统最终知道扣了没有"。
**非功能。** 绝不重复扣款，绝不扣了款却没记录；敏感信息不进我们的系统（PCI 范围最小化）。
