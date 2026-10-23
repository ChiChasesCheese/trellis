---
id: hl-os-crash-isolation
node: foundations.os-processes-threads-ipc
type: qa
step: 46
---
## Q
一个进程崩溃会影响同机另一个进程吗？同一进程里一个线程抛未捕获异常呢？

## A
一般不影响别的进程（地址空间隔离，除非共享资源且依赖对方）。

同一进程里一个线程抛未捕获的 `Exception` 只终止这个线程；但 `OutOfMemoryError` 等导致整个 JVM 崩溃，或原生代码段错误（`SIGSEGV`），整个进程退出，所有线程陪葬。
