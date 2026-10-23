---
id: hl-sd03-spsc-backpressure
node: system-design.sd03-low-latency-trading
type: qa
step: 11
---
## Q
SPSC 环（Disruptor 思想）的要点是什么？环满时，行情→分片、热线程→监控、热线程→日志三条通道各怎么处理？

## A
要点：序号只增不减，`index = seq & mask`；生产者 `setRelease(tail)`，消费者 `getAcquire(tail)`；cached index 减少对方缓存行读取；头尾字段之间填充 128 字节防伪共享。**批处理自平衡**：消费者落后时一次取走环中全部已发布事件逐条处理，积压越多每条摊到的同步开销越小，这是 Disruptor 在突发下比「一条一唤醒」的队列稳定的原因。

环满的背压策略因通道而异：
- 行情 → 分片：**不能丢也不能阻塞 Feed Handler**；环要足够大（按「最大突发 × 最大消费者停顿」算），仍满 ⟹ 严重故障，对该分片触发熔断（fail closed）并告警；
- 热线程 → 监控：**有损**（环满就丢指标），永不阻塞热线程；
- 热线程 → 日志：**不能丢**；环满说明 Journaler 落后，先告警，持续则熔断（宁可停止交易也不要「没记录的交易」）。
