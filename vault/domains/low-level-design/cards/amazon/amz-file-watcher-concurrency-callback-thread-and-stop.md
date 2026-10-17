---
id: amz-file-watcher-concurrency-callback-thread-and-stop
node: amazon.amz-file-watcher
type: qa
step: 8
tags: [grown]
---
## Q
在 Amazon 文件监听器设计里，后台线程怎么停？慢回调和「在回调里调用 stop()」各有什么问题？

## A
循环是 `while not stopped: poll(); stopped.wait(interval)`，`threading.Event.wait` 既是可中断的睡眠也是停止信号；`stop()` 置位后 `join`。回调跑在轮询线程上，所以慢回调推迟下一轮扫描，要隔离就让回调只入 `queue.Queue`、另一线程消费。回调里调用 `stop()` 时，当前线程就是轮询线程，`join` 自己会抛 `RuntimeError`，所以先判断不是当前线程再 join。
