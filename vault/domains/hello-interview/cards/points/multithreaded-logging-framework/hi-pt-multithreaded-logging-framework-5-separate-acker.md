---
id: hi-pt-multithreaded-logging-framework-5-separate-acker
node: qb.lld.multithreaded-logging-framework.points
type: qa
step: 5
---
## Q
**多线程日志框架 · 确认为什么独立一个线程**｜出自：多线程日志框架 › 整体设计

写入线程写完文件后，为什么不直接在自己线程里通知调用方，而要有独立的确认线程？

## A
**为什么。** 回调可能很慢（比如通知远端），放在写入线程里会拖慢落盘吞吐。
**机制。** 写完把这一批 Future 与可能的错误放进 `_to_ack`，确认线程成功则 `set_result(True)`，失败则 `set_exception`。
**顺序。** 确认线程按批顺序处理，确认顺序与写入顺序一致。
