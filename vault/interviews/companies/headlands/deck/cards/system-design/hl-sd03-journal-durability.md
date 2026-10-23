---
id: hl-sd03-journal-durability
node: system-design.sd03-low-latency-trading
type: qa
step: 21
---
## Q
日志怎么写才不拖慢热路径？三种故障下 mmap 文件里的数据各怎么样？日志格式是什么？

## A
- 热线程：事件 + 消费序号 + 硬件时间戳写入内存环（约几十 ns）；Journaler 线程：环 → 追加到 mmap 文件（页缓存）→ 异步复制到备机 / 归档。
- JVM / 进程崩溃（`kill -9`、OOM）：已写入页缓存的部分**仍在**（内核保管），不需要 fsync；
- 机器掉电 / 内核崩溃：未刷盘的页缓存丢失，需要 fsync 或已复制到另一台机器；
- 机房级故障：本机全部丢失，需要跨机房异步复制（延迟大，不进热路径），恢复靠交易所 + 清算对账。

概念对应物：Chronicle Queue（基于内存映射文件的堆外持久化队列）、Aeron Archive（录制 / 重放）、Aeron Cluster（Raft 复制状态机），面试说「思想相同」，不要承诺 API 细节。

日志格式：定长头（序号、事件类型、硬件时间戳、长度）+ 二进制载荷；只追加；按大小 / 时间切段；段头带校验。
