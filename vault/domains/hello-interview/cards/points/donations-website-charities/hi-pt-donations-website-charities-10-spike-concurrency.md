---
id: hi-pt-donations-website-charities-10-spike-concurrency
node: qb.sd.donations-website-charities.points
type: qa
step: 10
---
## Q
**限时捐款网站 · 尖峰下对 PSP 的并发控制**｜追问 · 出自：限时捐款网站 › 深入 5

尖峰 2,000 笔/秒时同步直连 PSP，线程会堵在网络调用上。怎样限制并发，超限后如何兜底？并发数怎么估？

## A
**估算。** 并发 = 吞吐 × 延迟，2,000 笔/秒 × 0.5 秒约 1,000 个并发。
**做法。** API 层无状态水平扩展；用信号量限制对 PSP 的并发调用数；超过时返回"排队中"，前端轮询 `GET /donations/{id}`，后台 worker 从队列取出继续调 PSP。
**取舍。** 用户多等几秒，但 PSP 不会被打爆，我们也不丢请求。
