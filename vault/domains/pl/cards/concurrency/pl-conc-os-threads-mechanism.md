---
id: pl-conc-os-threads-mechanism
node: concurrency.os-threads
type: qa
step: 5
---
## Q
在 Java、Rust、Python 里调用 `thread.start()` / `thread::spawn` 时，底层发生了什么？启动一个线程大约要花多久？

## A
三者做的事情基本相同：
1. 运行时向 OS 要一个线程：在 macOS 和 Linux 上是 `pthread_create`，内核创建一个新的调度实体。
2. OS 为它预留一段栈的虚拟地址（Rust 默认 2 MiB，Java 在 macOS 上 2 MB、Linux x64 上 1 MB）。物理页在第一次访问时才分配。
3. 新线程在自己的栈上运行传入的函数；函数返回，线程退出，栈归还。
4. 运行时同时维护自己的线程对象：Java 的 `Thread`、Rust 的 `JoinHandle`、Python 的 `threading.Thread`（Python 线程还要创建一个线程状态结构，并且必须拿到 GIL 才能跑字节码）。

启动加回收的耗时（在一台 12 核 Mac 上对「创建一个空线程再 `join`」循环 10000 次的平均值，一次测量）：

| 语言 | 每次 spawn + join |
|---|---|
| Java 平台线程 | 约 32 微秒 |
| Rust `thread::spawn` | 约 15 微秒 |
| Python `threading.Thread` | 约 19 微秒 |
| Go goroutine（对照） | 约 0.3 微秒 |

线程创建在十微秒量级，比一次函数调用贵上千倍。所以每次请求都新建一个线程的做法不适合高频场景，要用线程池（thread pool）：预先创建固定数量的线程，反复接任务。
