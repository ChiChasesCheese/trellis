---
id: hi-pt-multithreaded-logging-framework-1-pipeline-idea
node: qb.lld.multithreaded-logging-framework.points
type: qa
step: 1
---
## Q
**多线程日志框架 · 三线程流水线的目标**｜出自：多线程日志框架 › 需求

设计一个由接入、写入、确认三个专职线程组成的多线程日志框架。它要把什么和什么隔开？难点是哪几项？

## A
**要点。** 这是生产者-消费者流水线：用有界队列把调用方的低延迟与磁盘写入的慢隔开。
**难点。** 顺序、背压、批量刷盘、写成功后才确认，以及优雅关闭时不丢一条。
**接口。** `log(level, message)` 立刻返回 Future，落盘成功后在确认线程里完成。
