---
id: problems-thread-pool-shutdown-wait-false-only-abandons-queued
node: problems.components.thread-pool
type: qa
step: 4
tags: [grown]
---
## Q
线程池的 `shutdown(wait=False)` 应该立即返回、放弃工作。这个『放弃』具体指什么——连正在执行的任务也一起打断吗？

## A
不，只放弃**还没被 worker 取走**的任务（它们的 `Future` 收到一个表示『被放弃』的异常），正在执行的任务不受影响、会跑到自然结束。原因是 Python 没有安全终止一个正在运行的线程的官方 API——从外部强行打断一个线程可能在任意一条字节码之间发生，把共享数据结构留在『改了一半』的状态，比『等它跑完』危险得多。真正的取消需要任务体自己定期检查一个取消标志、在检查点主动退出，但 `submit()` 接受的是一个不透明的 `Callable`，线程池管不到它的内部实现。这和 `concurrent.futures.Executor.shutdown(cancel_futures=True)` 的真实语义一致——`cancel` 从来只覆盖排队中还没开始的任务，从不覆盖正在跑的。
