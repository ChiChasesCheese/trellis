---
id: hi-c-lld-logging-service-n05-logger-class
node: lld.problem-breakdowns.logging-service.notes
type: qa
step: 5
---
## Q
**日志库 · Logger 的状态与方法**｜摘要 · 必会

`Logger` 该持有什么状态？为什么不提供 `add_destination`？`log` 里哪些值在哪里取？

## A
- **只有一个字段：** 目的地列表，构造时存一份不可变副本。这是需求推出的唯一状态。
- **为什么不可变：** 配置只在启动时设置一次，所以遍历列表不用加锁。如果留一个可变的 `add_destination`，就得为遍历加锁，却没有换来任何需求要求的能力。同理不要 setter、builder。
- **方法：** `log(level, message)` 加 `debug/info/warn/error/fatal` 五个一行的委托。便捷方法的价值是调用点简洁：日志器会被成千上万处调用，`info("..")` 比 `log(INFO, "..")` 少一份噪音。
- **`log` 做什么：** 在调用线程里取当前时间和线程名，配上调用方给的级别和消息造一条 `Record`，顺序遍历每个目的地的 `write`。
- **不做什么：** Logger 上不过滤级别（阈值在目的地，过滤跟着阈值走），不改任何自己的状态，不开线程并行分发（异步是另一个决定）。
