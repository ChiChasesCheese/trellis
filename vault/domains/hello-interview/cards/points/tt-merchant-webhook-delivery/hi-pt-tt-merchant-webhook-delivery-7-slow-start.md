---
id: hi-pt-tt-merchant-webhook-delivery-7-slow-start
node: tt.sd.tt-merchant-webhook-delivery.points
type: qa
step: 7
---
## Q
**商户回调（Webhook）投递系统 · 恢复时不打垮商户**｜出自：商户回调（Webhook）投递系统 › 深入 2

商户宕机一小时后恢复，36 万条积压怎么放出才不把它再打垮？

## A
**做法。** 熔断探测成功后慢启动，并发额度从 1 逐步升到上限；重试时间加抖动打散；积压按创建时间从旧到新放出。
**长期失败。** 超过 3 天重试窗口则自动停用端点并通知商户，事件仍留在日志里供其修好后补拉。
