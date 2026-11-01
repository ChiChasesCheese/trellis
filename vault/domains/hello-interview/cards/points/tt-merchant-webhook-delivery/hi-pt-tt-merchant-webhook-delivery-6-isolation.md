---
id: hi-pt-tt-merchant-webhook-delivery-6-isolation
node: tt.sd.tt-merchant-webhook-delivery.points
type: qa
step: 6
---
## Q
**商户回调（Webhook）投递系统 · 按端点隔离与熔断**｜出自：商户回调（Webhook）投递系统 › 深入 2

某个端点每次超时 10 秒，工人线程被占满，其他商户首次投递变慢。怎么隔离？

## A
**选项。** 全局线程池会被占满；每商户一个队列太多（数十万）；选共享队列加每端点并发额度（同时在途不超过 5 个）加令牌桶加熔断。
**熔断。** 连续失败 N 次（如 10）转 degraded，之后只定期发一个探测请求，成功才恢复；熔断期间事件只写投递表，不占工人。
**公平。** 再给每商户总投递速率上限。
