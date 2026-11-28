---
id: hi-c-lld-logging-service-n10-final-design
node: lld.problem-breakdowns.logging-service.notes
type: qa
step: 10
---
## Q
**日志库 · 最终类设计与职责划分**｜摘要 · 必会

最终的类图怎么放？每个类为什么只有一个变化原因？

## A
- **六块：** `LogLevel`（枚举）、`LogRecord`（不可变记录）、`Formatter`（序列化接口）、`Sink`（输出接口）、`Destination`（组合前三者加阈值）、`Logger`（编排）。
- **关系：** `Logger` 持有多个 `Destination`；每个 `Destination` 持有一个 `Formatter`、一个 `Sink`；每次 `log` 造一条 `Record`，同一条交给所有目的地。没有环、没有反向引用，除了各目的地自己的资源外没有共享可变状态。
- **一个变化轴一个类：** 加格式只动 `Formatter` 的实现，加输出位置只动 `Sink` 的实现，加目的地配置只是新的构造参数，`Logger` 不动。这才是单一职责在实践里的含义：不是"类越小越好"，而是"一个类只有一个变化原因"。
- **扩展点：** 新 sink、新 formatter。
