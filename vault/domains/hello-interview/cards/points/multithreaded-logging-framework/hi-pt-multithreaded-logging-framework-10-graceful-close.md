---
id: hi-pt-multithreaded-logging-framework-10-graceful-close
node: qb.lld.multithreaded-logging-framework.points
type: qa
step: 10
---
## Q
**多线程日志框架 · 优雅关闭与崩溃边界**｜出自：多线程日志框架 › 深入 5

如何保证关闭时已接收的日志全部写完？进程被强制终止又会怎样？

## A
**关闭。** `close` 在互斥保护下置位已关闭并放入毒丸，其后的 `log` 被拒绝；毒丸依次通过三级线程，每一级先处理完毒丸之前的数据再传给下一级；`close` 等待三线程结束再关文件。
**守护线程。** 线程设为 daemon，强制终止时队列中日志会丢，所以退出路径要调用 `close` 或注册退出钩子。
**kill -9。** 未落盘的会丢；更强保证用同步写加 fsync 或预写日志，是吞吐与持久性的取舍。
