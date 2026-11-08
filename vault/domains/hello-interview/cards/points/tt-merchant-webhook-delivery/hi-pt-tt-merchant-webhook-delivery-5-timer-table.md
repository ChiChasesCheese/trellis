---
id: hi-pt-tt-merchant-webhook-delivery-5-timer-table
node: tt.sd.tt-merchant-webhook-delivery.points
type: qa
step: 9
---
## Q
**商户回调（Webhook）投递系统 · 重试计时用投递表**｜追问 · 出自：商户回调（Webhook）投递系统 › 深入 6

重试的等待放在队列延迟消息里，还是投递表？

## A
**选用。** 投递表加调度器：每秒扫 `next_attempt_at <= now` 的 failed 投递并重新入队，索引 `(status, next_attempt_at)`；工人不睡眠等待。
**为什么。** 每天约 2000 万事件，算上重试也只是几千万次投递，量很小，投递表本来就要存状态，停用、手动重发、改期都是改一行；慢商户不会占住分区。
