---
id: pl-conc-os-threads-best-practice
node: concurrency.os-threads
type: qa
step: 8
---
## Q
在 Java、Rust、Python 里直接 `new Thread` / `thread::spawn` 通常被认为是坏习惯，资深工程师的做法是什么，为什么？

## A
线程创建约十几到几十微秒，又会占用栈、内核结构，还有系统上限，直接按需创建有四个问题：成本、无上限、结果和异常丢失、生命周期难管。通行做法：

1. **用线程池，大小有界。** Java `Executors`/`ThreadPoolExecutor`（自定义有界队列和拒绝策略），Python `ThreadPoolExecutor`。线程复用省掉创建成本，上限保护系统：线程池满了是在入口处排队或拒绝，而不是把机器拖到 `unable to create native thread`。
2. **任务返回 `Future`，在汇合点处理异常。** 裸线程里的异常只打印不传播；`future.get()` / `.result()` 会重新抛出。Rust 的 `join()` 返回 `Result`，同样不要 `unwrap` 掉。
3. **给线程起名字。** 线程转储和日志里没有名字就很难排查（Java `ThreadFactory`、Python `name=`、Rust `Builder::name`）。
4. **让线程的生命周期被一个作用域包住。** Rust `thread::scope` 保证所有子线程在作用域结束前 join，因此可以安全地借用局部变量；Java 21+ 的结构化并发、Python 的 `with ThreadPoolExecutor` 同理。
5. **线程数的依据**：CPU 密集约等于核数；阻塞 I/O 则由下游容量决定。需要几万级别的并发时，不要加线程，换虚拟线程或 async。

什么时候打破：长期运行、职责固定的后台线程（日志刷盘、心跳）可以直接创建并命名，但要有关闭路径。
