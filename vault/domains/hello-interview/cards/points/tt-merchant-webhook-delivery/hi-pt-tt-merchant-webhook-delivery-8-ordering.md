---
id: hi-pt-tt-merchant-webhook-delivery-8-ordering
node: tt.sd.tt-merchant-webhook-delivery.points
type: qa
step: 8
---
## Q
**商户回调（Webhook）投递系统 · 顺序：不保证全局顺序**｜出自：商户回调（Webhook）投递系统 › 深入 3

同一笔支付的「已授权、已扣款、已退款」第一个失败重试会在第二个之后到达。顺序怎么处理？

## A
**默认。** 不保证顺序，事件带 `resource_version` 和创建时间，商户忽略旧版本或调查询接口，吞吐最高。
**可选。** 对明确要求顺序的端点按 `ordering_key = 资源 ID` 串行，调度器只放出该 key 下编号最小的未完成投递，队头阻塞只在这个资源上。
**否决。** 整个端点严格 FIFO，一个失败卡住所有事件 3 天。
