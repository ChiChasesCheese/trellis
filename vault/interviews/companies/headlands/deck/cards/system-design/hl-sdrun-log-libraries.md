---
id: hl-sdrun-log-libraries
node: system-design.how-to-run
type: qa
step: 25
---
## Q
Chronicle Queue、Aeron、LMAX Disruptor 各是什么？它们对应设计里的哪些概念？

## A
- **Chronicle Queue**：基于内存映射文件的堆外持久化队列；
- **Aeron**：可靠 UDP / IPC 传输；Aeron Archive 做录制与重放，Aeron Cluster 在其上做 Raft 复制状态机；
- **LMAX Disruptor**：环形缓冲区 + 序号 + 单写者，单线程业务处理器每秒可处理约 600 万订单。

它们是概念对应物，不要求背 API；用来说明「日志 + 单写者 + 重放」不是空谈。
