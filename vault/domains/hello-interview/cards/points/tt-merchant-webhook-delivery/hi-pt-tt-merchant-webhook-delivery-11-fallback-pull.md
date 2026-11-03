---
id: hi-pt-tt-merchant-webhook-delivery-11-fallback-pull
node: tt.sd.tt-merchant-webhook-delivery.points
type: qa
step: 10
---
## Q
**商户回调（Webhook）投递系统 · 兜底：事件日志与重发**｜追问 · 出自：商户回调（Webhook）投递系统 › 深入 6

追问：商户说没收到通知，平台怎么补？webhook 在整体里是什么地位？

## A
**兜底。** 事件日志保留 30 天，商户按 `GET /events?after=<cursor>` 补拉；控制台看每次 Attempt 的状态码、耗时，可手动或批量重发。
**地位。** webhook 是加速器，不是商户状态的唯一依据；收款侧要有轮询兜底，回调只是提示。
**否决。** 同步等商户处理完再回支付结果：商户慢会拖慢支付。
