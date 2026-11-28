---
id: hi-c-lld-coordination-x05-polling-cost
node: lld.concurrency.coordination.exam
type: qa
step: 5
---
## Q
**并发协调 · 轮询的成本**｜考点 · 必会

工人用 `sleep(0.1)` 轮询空队列。任务随机到达，平均要额外等多久？缩短到 `sleep(0.001)` 又有什么代价？

## A
- **平均额外延迟：** 约 50 毫秒（睡眠周期的一半），最坏接近 100 毫秒
- **缩短睡眠：** 延迟降下来，但每个工人每秒醒 1000 次，空闲时也占 CPU
- **根本解法：** 阻塞等待，空闲零 CPU，来活立刻醒
- **结论：** 轮询永远在延迟和 CPU 之间取舍，阻塞队列去掉了这个取舍
