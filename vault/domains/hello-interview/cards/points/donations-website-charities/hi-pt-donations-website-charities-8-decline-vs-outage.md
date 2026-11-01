---
id: hi-pt-donations-website-charities-8-decline-vs-outage
node: qb.sd.donations-website-charities.points
type: qa
step: 8
---
## Q
**限时捐款网站 · 区分被拒绝与没拿到结果**｜出自：限时捐款网站 › 深入 3

支付失败有两类：卡被拒绝，和没拿到结果。哪一类才值得换 PSP 重试？一笔结果未知的交易能直接转给备用 PSP 吗？

## A
**区分。** 被拒绝是业务结果，卡本身有问题，换 PSP 没意义，应让用户换卡；没拿到结果才可能是 PSP 故障。
**切换。** 对主 PSP 做熔断，打开后新请求路由到备用 PSP。
**易错。** 结果未知的交易在查清之前绝不能转给另一家 PSP 重发，否则可能扣两次；先查询或取消，再改路由。
