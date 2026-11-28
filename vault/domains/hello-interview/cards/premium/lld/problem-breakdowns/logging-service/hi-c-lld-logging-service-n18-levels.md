---
id: hi-c-lld-logging-service-n18-levels
node: lld.problem-breakdowns.logging-service.notes
type: qa
step: 15
---
## Q
**日志库 · 各级别的期望**｜摘要 · 必会

初级、中级、高级候选人在日志库上分别被期望做到什么？

## A
- **初级：** 拆出 `Logger`、不可变 `LogRecord`、五值 `LogLevel` 枚举；`log()` 造记录并分发给每个目的地，目的地丢弃低于阈值的记录。有基本的错误处理，空消息或越界级别不崩。第一版把格式和目的地耦合（如 `JsonFileDestination`）也可以，被追问后能看到 2D 类爆炸即可。
- **中级：** 不用提示就想到"任意格式配任意目标"要组合，抽出 `Formatter` 接口，一个 `Destination` 类取代 N×M 个子类；知道 `LogRecord` 要独立以便以后加日志器名、请求 ID。并发能对话并在提示后到达合理方案。
- **高级：** 系统性思考。主动比较继承和组合并落到 `Sink`，说清为什么高层类不依赖具体 sink 和 formatter；自己想到时间戳放在 `log` 入口；不用提示就是每目的地一把锁，解释为什么全局锁错（慢文件拖住即时的控制台），格式化为什么在锁外；吞异常并写 stderr 诊断。早完成的话能谈异步（队列、溢出、关闭）和层级 logger（注册表是合理的全局、沿父链继承、缓存有效级别）。
