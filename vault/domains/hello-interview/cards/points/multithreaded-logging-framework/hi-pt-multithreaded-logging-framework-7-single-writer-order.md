---
id: hi-pt-multithreaded-logging-framework-7-single-writer-order
node: qb.lld.multithreaded-logging-framework.points
type: qa
step: 7
---
## Q
**多线程日志框架 · 为什么三个专职线程而不是线程池**｜必会 · 出自：多线程日志框架 › 深入 2

日志框架为什么用单接入线程加单写入线程而不是线程池？想要多个写入线程怎么保持顺序？

## A
**原因。** 单接入加单写入天然保证 FIFO。
**扩展。** 多个写入线程要保持顺序，就得按分区（例如按日志来源哈希）分别写不同文件。
**对比。** 多线程加锁写同一文件简单，但所有业务线程争用锁并直接承担磁盘延迟；单写线程无锁竞争且利于成批。
