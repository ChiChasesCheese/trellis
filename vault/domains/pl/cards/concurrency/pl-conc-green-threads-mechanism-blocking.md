---
id: pl-conc-green-threads-mechanism-blocking
node: concurrency.green-threads
type: qa
step: 5
---
## Q
用户态线程遇到阻塞调用时，运行时怎样避免“一个阻塞卡住整个调度器”？
Go 在只有一个 P 时跑 4 个阻塞系统调用、Java 虚拟线程在 `synchronized` 里睡眠，实测耗时各是多少？

## A
用户态线程方案最大的风险是：如果一个用户态线程做了阻塞的系统调用，承载它的 OS 线程就被内核挂起，这个 OS 线程上排队的其他用户态线程全部停摆。运行时必须解决这个问题，两种办法：
1. **拦截**：把阻塞库调用改成“登记等待 + 挂起当前用户态线程 + 去跑别的”，由事件轮询器（epoll/kqueue）在就绪时唤醒（Go 的网络 I/O、Java 虚拟线程的 `sleep`/I/O/队列）；
2. **交出资源**：无法拦截的阻塞系统调用，运行时把执行权（Go 的 P）交给另一个线程，让其他任务继续，必要时新建 OS 线程。

实测一（Go，`GOMAXPROCS(1)` 只有一个 P，4 个 goroutine 各做一次 0.5 秒的阻塞系统调用 `select`，一次测量）：总耗时 **0.65 秒**，对比 4 个 `time.Sleep` 的 **0.50 秒**。若阻塞调用占着唯一的 P，应该串行 2 秒；实际没有，因为线程陷入内核后运行时把 P 交给了新的 OS 线程。代价是多开了几个 OS 线程，所以比纯 `Sleep` 稍慢。

实测二（Java 25，虚拟线程调度器限制为 1 个载体线程：`-Djdk.virtualThreadScheduler.parallelism=1 -Djdk.virtualThreadScheduler.maxPoolSize=1`，4 个虚拟线程各睡 0.5 秒）：普通 `sleep` 约 **0.66 秒**，`synchronized` 块里 `sleep` 约 **0.64 秒**。两者都不是串行的 2 秒，说明虚拟线程在阻塞时卸载了栈，载体线程去跑别人。

历史细节：JDK 21 里在 `synchronized` 块内阻塞会把虚拟线程**钉住**（pinning）在载体线程上，载体线程被一起挂起；JDK 24 起（JEP 491）修复了这一点，所以本实测没有变慢。仍然会钉住的情形包括正在执行原生方法（JNI/FFM 调用）时阻塞。

结论：用户态线程方案的成败取决于**运行时和标准库为它改造了多少阻塞点**。Go 从一开始就全面改造，Java 经历了二十年才补上，Python/Rust 没有这条路。
