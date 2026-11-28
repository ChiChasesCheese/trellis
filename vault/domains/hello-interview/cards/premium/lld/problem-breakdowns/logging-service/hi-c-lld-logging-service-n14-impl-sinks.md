---
id: hi-c-lld-logging-service-n14-impl-sinks
node: lld.problem-breakdowns.logging-service.notes
type: qa
step: 16
---
## Q
**日志库 · Formatter 与 Sink 的实现要点**｜摘要 · 追问

`PlainTextFormatter`、`JsonFormatter`、`FileSink` 的实现有哪些容易忽略的点？

## A
- **两个 formatter：** 都是纯函数。纯文本拼接时间戳、`[级别]`、`[线程名]`、消息；JSON 编码四个字段。
- **FileSink 只打开一次：** 构造时以追加模式打开文件并保留句柄，不要每次写都重新打开；`open` 系统调用的开销会远超一次写。程序关闭或显式 `close()` 时再关。
- **刷新：** 实际的文件 sink 应在每次写后（或每隔一小段时间）`flush()`，否则最近几行还在操作系统缓冲里进程就崩了。大多数语言默认只在关闭时刷新，对日志而言恰恰是最没用的时刻：你要的是崩溃之前的日志。
- **缓冲、编码、系统级刷盘：** 属于底层输出流的事，sink 只调用正确的方法。
