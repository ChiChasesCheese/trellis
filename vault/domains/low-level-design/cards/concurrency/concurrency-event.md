---
id: concurrency-event
node: concurrency.primitives
type: qa
step: 4
---
## Q
`threading.Event` 解决的是什么问题？它和自己写一个 `while not flag: time.sleep(0.01)` 轮询循环比，好在哪？

## A
`Event` 封装了一个线程间共享的布尔标志，配上 `wait()`：`set()` 把标志置 `True` 并唤醒所有在 `wait()` 上阻塞的线程，`clear()` 置回 `False`，`is_set()` 查询当前值，`wait(timeout=...)` 阻塞到标志被置位或超时为止。典型场景是"一个线程等另一个线程完成初始化/收到关闭信号"这种一次性或阶段性信号。

比起自己写轮询循环，`Event.wait()` 是真正阻塞的，不占 CPU、也没有轮询间隔带来的延迟；而手写轮询既浪费 CPU，又在 `time.sleep` 间隔内引入了不必要的响应延迟。误用：`Event` 只是一个一次性开关，不能像 `Condition` 那样表达"每次有新数据就唤醒一次"这种反复发生、带数据的信号。
