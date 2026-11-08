---
id: hi-pt-tt-per-merchant-rate-limit-5-retry-after-cost
node: tt.lld.tt-per-merchant-rate-limit.points
type: qa
step: 5
---
## Q
**按商户限流 · 等待时间与超额 cost**｜必会 · 出自：按商户限流 › 深入 2

被拒时 `retry_after` 怎么算？`cost` 超过突发上限时怎么处理？

## A
**等待时间。** 缺少的令牌数除以速率。默认限额速率 5/秒、突发 10、桶初始是满的时，瞬间连发的第 11 次请求缺 1 个令牌，retry_after = 1÷5 = 0.2 秒。
**超额。** `cost` 大于突发上限永远凑不够，直接返回无穷大的等待时间并拒绝，而不是让客户端空等。
**权重。** 批量接口一次消耗多个令牌。
