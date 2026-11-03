---
id: hi-pt-donations-website-charities-9-auth-capture
node: qb.sd.donations-website-charities.points
type: qa
step: 9
---
## Q
**限时捐款网站 · 授权与请款分两步**｜追问 · 出自：限时捐款网站 › 深入 4

支付可以一步完成扣款，也可以先授权（authorize）后请款（capture）。分两步对备用通道切换有什么好处，代价是什么？

## A
**好处。** 授权失败可以直接换通道，扣款只在确定后做一次，切换更安全。
**代价。** 多一次调用，延迟加倍。
**补充。** 备用支付方式还可提供钱包（Apple Pay、PayPal 等），卡支付失败时前端提示改用。
