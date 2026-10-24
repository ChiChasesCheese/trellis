---
id: pl-conc-os-threads-pitfall-limit
node: concurrency.os-threads
type: qa
step: 9
---
## Q
「每个连接一个线程」（thread-per-connection）的服务器为什么扛不住上万个并发连接？Java 一直开线程会得到什么错误，内存成本是多少？

## A
每个 OS 线程都要内核结构、一段栈，以及调度和切换的开销，而且系统对线程数有上限。一个线程在大部分时间里只是阻塞等待 I/O，却一直占着这些资源。

一次实验（macOS、JDK 25，一次测量）：不断创建会阻塞等待的线程：
```java
CountDownLatch l = new CountDownLatch(1);
while (true) {
    Thread t = new Thread(() -> { try { l.await(); } catch (Exception e) {} });
    t.setDaemon(true); t.start();
}
```
结果：在大约 4070 个线程时抛出
`java.lang.OutOfMemoryError: unable to create native thread: possibly out of memory or process/resource limits reached`。这台机器的内核上限 `kern.num_taskthreads` 是 4096。进程常驻内存（RSS）约 296 MB，平均每个线程约 70 KB 的真实占用，另外还有预留的虚拟栈地址。

要点：
- 错误信息写的是 `OutOfMemoryError`，但根因常常不是堆满，而是线程数撞上了 OS 上限或虚拟地址预留。
- Linux 上的上限通常更高（`ulimit -u`、`/proc/sys/kernel/threads-max`），但数万个线程时调度开销已经明显。
- 出路有三条：线程池限制并发、非阻塞 I/O 加事件循环（async）、轻量级线程（goroutine、Java 虚拟线程）。
