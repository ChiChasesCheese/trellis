---
id: hi-pt-tt-merchant-webhook-delivery-9-signature
node: tt.sd.tt-merchant-webhook-delivery.points
type: qa
step: 6
---
## Q
**商户回调（Webhook）投递系统 · 签名、重放与密钥轮换**｜必会 · 出自：商户回调（Webhook）投递系统 › 深入 3

商户怎么验证通知确实来自平台？怎么防重放？密钥怎么轮换？

## A
**签名。** 每端点独立密钥，对 `t + "." + 原始请求体` 算 HMAC-SHA256 放 `X-Signature`；商户常量时间比较，拒绝时间戳偏差超 5 分钟的请求；必须对原始字节签名，不能解析后重新序列化。
**轮换。** 一段时间内新旧密钥并存，头里放两个签名，任一通过即可。想防平台伪造可改非对称签名。
