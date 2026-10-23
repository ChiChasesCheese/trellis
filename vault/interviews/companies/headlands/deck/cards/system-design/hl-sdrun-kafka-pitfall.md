---
id: hl-sdrun-kafka-pitfall
node: system-design.how-to-run
type: qa
step: 6
---
## Q
把交易系统答成「Kafka → Flink → Redis」为什么是常见的坑？什么情况下消息队列可以出现？

## A
这是把交易系统答成大厂的实时流处理：每一跳是 ms 级，整条链路比微秒级预算**大三个数量级**。

除非题目明确是**离线 / 准实时**的侧链路（研究、监控、对账、落盘），不要把消息队列放到热路径上。
