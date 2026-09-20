---
id: kafka-practice-g1gc-small-heap-tuning
node: practice.sizing-tuning
type: qa
step: 6
source: kafka-2e
---
## Q
Kafka broker 通常只需要几 GB 的堆内存（大部分系统内存要留给页面缓存），在这种「堆内存不大、垃圾回收效率本身就比较高」的前提下，为什么建议把 G1GC 的 `MaxGCPauseMillis`（目标停顿时间，默认200毫秒）和 `InitiatingHeapOccupancyPercent`（触发新一轮回收的堆占用率阈值，默认45%）都调得比默认值更小？

## A
G1GC 会根据配置的目标停顿时间和堆占用率阈值自动决定每一轮垃圾回收的频率和范围；Kafka 使用堆内存的方式清晰、待回收的垃圾对象处理效率本身就比较高，不需要等默认阈值触发再进行大规模回收。把 `InitiatingHeapOccupancyPercent` 调低（比如从45调到35），意味着堆内存使用率更低的时候就提前启动新一轮回收，避免等到堆内存快用满时才回收、造成一次性回收的对象过多、单次停顿时间被拉长；把 `MaxGCPauseMillis` 调低（比如从200毫秒调到20毫秒），是明确告诉 G1GC 每次停顿要更短，配合更小的堆内存，能让回收更频繁、更细粒度地进行，从而把每次停顿对 Kafka 正常处理请求造成的影响降到最低。
