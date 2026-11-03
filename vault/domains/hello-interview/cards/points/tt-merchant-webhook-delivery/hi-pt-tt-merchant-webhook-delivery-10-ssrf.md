---
id: hi-pt-tt-merchant-webhook-delivery-10-ssrf
node: tt.sd.tt-merchant-webhook-delivery.points
type: qa
step: 11
---
## Q
**商户回调（Webhook）投递系统 · 防 SSRF**｜加分 · 出自：商户回调（Webhook）投递系统 › 深入 7

商户可以填任意回调 URL，平台怎么避免被利用访问内网？

## A
**做法。** 要求 HTTPS；每次发送前解析域名，拒绝私网、回环、链路本地和云元数据地址（如 169.254.169.254），并用解析出的那个 IP 去连，防校验与连接之间被改解析；出站经专用出口代理；不跟随重定向；响应只读前 1 KB。
**负载。** 瘦事件，不带卡号等敏感数据，只带标识。
