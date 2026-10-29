---
id: uth-kafka-consumer-group-2-range-vs-roundrobin
node: kafka.consumer-group
type: qa
step: 2
---
## Q
**Range 与 RoundRobin：谁分得更匀**｜Kafka · 4.0

2 个主题各 3 个分区，2 个消费者都订阅全部主题。Range 和 RoundRobin 各分出什么结果？

## A
**结构。** Range 按主题逐个分：每个主题里分区数 `n / c` 取整，前 `n % c` 个消费者多拿一个。RoundRobin 把所有分区排成一队轮流发牌。

**细节。** 官方文档里的例子：

```
Range:      C0 [t0p0 t0p1 t1p0 t1p1]   C1 [t0p2 t1p2]
RoundRobin: C0 [t0p0 t0p2 t1p1]        C1 [t0p1 t1p0 t1p2]
```

- 客户端默认策略是 `[RangeAssignor, CooperativeStickyAssignor]`（3.0 起，之前只有 Range）。

**坑。** Range 对每个主题都让排在前面的消费者多拿，主题越多、分区数越除不尽，前面的消费者越吃重。

**对应 LeetCode：** LC 725 分隔链表
