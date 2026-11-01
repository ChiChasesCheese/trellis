---
id: hi-pt-multithreaded-logging-framework-8-io-failure
node: qb.lld.multithreaded-logging-framework.points
type: qa
step: 8
---
## Q
**多线程日志框架 · 写入失败如何通知调用方**｜出自：多线程日志框架 › 深入 3

写入线程遇到 I/O 错误时怎么处理？为什么 `log` 本身不抛 I/O 异常？

## A
**处理。** 这一批的 Future 全部以异常完成；可选重试几次，仍失败则落入备用位置（死信文件或标准错误输出）。
**为什么。** 日志框架自己出错不能让业务线程崩溃，所以错误通过 Future 传递，而不是从 `log` 抛出。
