---
id: hi-pt-tt-merchant-webhook-delivery-4-backoff
node: tt.sd.tt-merchant-webhook-delivery.points
type: qa
step: 4
---
## Q
**商户回调（Webhook）投递系统 · 退避重试与响应语义**｜出自：商户回调（Webhook）投递系统 › 深入 1

失败重试的间隔怎么定？不同状态码怎么处理？

## A
**退避。** 依次 1 分钟、5 分钟、30 分钟、2 小时、6 小时、12 小时，之后每 24 小时一次，到 72 小时截止；每个间隔加 ±20% 抖动。
**语义。** 2xx 成功；3xx 视为失败（不跟随重定向）；4xx、5xx 都重试，429 和 503 遵守 `Retry-After`；410 直接停用端点。
