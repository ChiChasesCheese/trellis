---
id: hi-c-sd-temporal-x07-worker-crash
node: sd.deep-dives.temporal.exam
type: qa
step: 7
---
## Q
**Temporal · 缓存了 Workflow 的 worker 崩溃会怎样**｜考点 · 必会

worker A 缓存了某订单 Workflow 的状态，所有该订单的任务都粘性地发给它。A 突然崩溃。订单会丢吗？会有什么代价？

## A
- **不会丢：** 事件历史在持久存储里，状态才是真相；A 的缓存只是优化。
- **过程：** A 不再轮询，发给它的粘性队列的任务无人取，等一段时间（粘性任务的超时）后，下一个 Workflow Task 被改发到普通 Task Queue，由 worker B 拾取，B 用事件历史从头重放、重建 Workflow 状态，再继续。
- **代价：** 一次额外的延迟（等粘性超时），加上 B 上一次完整重放的 CPU 开销；Workflow 历史越长越贵。
- **如果 A 上的 Activity 正在执行：** 该 Activity 按超时或心跳丢失判定失败，然后重试，所以 Activity 要幂等。
- **结论：** 正确性来自持久历史，缓存和粘性只影响性能。
