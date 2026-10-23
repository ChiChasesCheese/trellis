---
id: hl-j11-cancel-needs-interrupt
node: java21.j11-structured-concurrency
type: qa
step: 18
---
## Q
子任务是 `while (true) { x = heavy(x); }`（纯计算，不检查中断），别的子任务失败后，`StructuredTaskScope` 会发生什么？怎么设计子任务？

## A
不会被取消：`shutdown()` 只是 `interrupt()`，纯计算不响应；调用不响应中断的库（老式阻塞 I/O）也停不下来。而 `close()` 会等所有子线程结束，所以 `try` 块就**卡在 `close()`** 直到它算完（这里是永远）。

设计子任务要保证可中断：
- 在阻塞调用上让 `InterruptedException` 往外传，别吞掉；
- 计算循环里检查 `Thread.currentThread().isInterrupted()`。
