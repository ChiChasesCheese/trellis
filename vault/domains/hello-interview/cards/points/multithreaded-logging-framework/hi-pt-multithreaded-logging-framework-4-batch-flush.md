---
id: hi-pt-multithreaded-logging-framework-4-batch-flush
node: qb.lld.multithreaded-logging-framework.points
type: qa
step: 4
---
## Q
**多线程日志框架 · 批量刷盘**｜出自：多线程日志框架 › 整体设计

写入线程为什么要成批写入？批量怎么凑，持久性怎么保证？

## A
**做法。** 取到第一条后在短时间 `batch_wait` 内继续取，最多凑够 `batch_size` 条，一次写入并 `flush`，需要更强持久性时再 `fsync`。
**为什么。** 把每条一次系统调用摊薄成每批一次，是吞吐的关键。
**强度。** 写应用缓冲区、flush 到操作系统缓存、fsync 到磁盘，越强越慢；按批 fsync（组提交）是标准做法，一批共享一次刷盘。
