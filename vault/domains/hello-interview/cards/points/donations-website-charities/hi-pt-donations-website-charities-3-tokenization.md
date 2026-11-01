---
id: hi-pt-donations-website-charities-3-tokenization
node: qb.sd.donations-website-charities.points
type: qa
step: 3
---
## Q
**限时捐款网站 · 令牌化与 PCI 范围**｜出自：限时捐款网站 › 核心实体与接口

捐款网站要接收银行卡信息，但不能让服务器碰卡号。付款信息应该如何采集？这样做的好处是什么？

## A
**做法。** 付款信息由 PSP 的前端组件（hosted fields / Elements）直接采集，浏览器向 PSP 换取一次性令牌（token），再把令牌发给我们。
**好处。** 我们的服务器从头到尾没见过卡号，PCI 合规范围最小。
**接口。** `POST /donations` 体里带 `donationId`、`charityId`、金额、支付令牌、邮箱。
