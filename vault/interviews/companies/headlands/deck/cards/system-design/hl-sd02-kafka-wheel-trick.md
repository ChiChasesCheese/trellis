---
id: hl-sd02-kafka-wheel-trick
node: system-design.sd02-job-scheduler
type: qa
step: 17
---
## Q
Kafka 的时间轮实现有什么技巧？什么时候值得用？

## A
不让线程每个 tick 醒一次，而是把「非空的槽」放进一个 `DelayQueue`，线程在 `DelayQueue.poll(timeoutMs, ...)`（带超时的 poll）上睡到下一个非空槽到期。稀疏时省 CPU。

本调度器 tick = 10 ms，每秒 100 次空转的成本可忽略；若 tick 取 1 ms 才值得这样做。
