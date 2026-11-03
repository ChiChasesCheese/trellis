---
id: hi-pt-multithreaded-logging-framework-3-seq-in-intake
node: qb.lld.multithreaded-logging-framework.points
type: qa
step: 3
---
## Q
**多线程日志框架 · 序号集中在接入线程分配**｜必会 · 出自：多线程日志框架 › 整体设计

日志在文件中的顺序要与接入顺序一致。序号由谁分配？时间戳由谁取？为什么？

## A
**序号。** 集中由单个接入线程分配全局递增序号，不需要跨线程原子计数，文件里的顺序就等于接入顺序。
**时间戳。** 在调用方线程取，最贴近事件发生时刻。
**易错。** 二者并发下可能略有出入（时间戳小的序号反而大），查询以序号为准，序号代表落盘顺序。
