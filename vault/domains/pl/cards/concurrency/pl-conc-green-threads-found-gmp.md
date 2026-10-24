---
id: pl-conc-green-threads-found-gmp
node: concurrency.green-threads
type: qa
step: 3
---
## Q
Go 的 GMP 调度器里 G、M、P 分别是什么？一个 goroutine 阻塞在系统调用或 channel 上时，调度器怎样让其他 goroutine 继续跑？

## A
- **G**（goroutine）：一个待执行的任务，包含自己的栈和状态。栈初始约 2 KB，放在堆上；栈满时运行时分配一块两倍大小的新栈并把内容拷过去，所以可以从 2 KB 长到 GB。
- **M**（machine）：一个 OS 线程，真正执行代码。
- **P**（processor）：执行 Go 代码所需的「许可证」和本地资源，里面有一个本地运行队列。P 的数量等于 `GOMAXPROCS`，默认是 CPU 核数。

规则：一个 M 必须持有一个 P 才能运行 G。每个 P 从自己的本地队列取 G；队列空了就去全局队列取，或从别的 P 那里**窃取**一半（work stealing）。

阻塞时：
1. **channel / 锁 / `time.Sleep` 阻塞**：只有这个 G 被挂起（放进等待队列），M 和 P 立刻去取下一个 G，没有线程被阻塞。
2. **阻塞的系统调用**：M 本身会陷在内核里，运行时（sysmon 监控线程）发现后把 P 从这个 M 上拿走，交给另一个空闲的或新建的 M 继续跑队列。
3. **网络 I/O**：goroutine 看似阻塞，其实底层 fd 是非阻塞的，由网络轮询器（netpoller，epoll/kqueue）统一等待，就绪后再把 G 放回队列。

数字（一次测量，100 万个阻塞 goroutine）：每个栈 2.0 KB，进程向系统申请的内存合计约 2.8 GB（含 G 结构等运行时开销，即每个约 2.7 KB）。
