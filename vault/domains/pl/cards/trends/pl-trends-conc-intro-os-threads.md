---
id: pl-trends-conc-intro-os-threads
node: trends.concurrency-evolution
type: qa
step: 2
---
## Q
操作系统线程（OS thread）是什么？为什么“一个请求一个线程”在并发连接数到几千以后就撑不住，真实的上限是什么样子？

## A
**是什么**：线程是操作系统调度的最小执行单位。每个线程有自己的寄存器、程序计数器和一块**栈**，操作系统用时间片轮流把 CPU 分给它们。Java 的 `Thread`、Python 的 `threading.Thread`、Rust 的 `std::thread` 默认都是一对一映射到系统线程。

**成本**：
1. **栈内存**：系统为每个线程预留栈空间（常见 1 到 8 MB 的虚拟地址，其中实际使用的部分按需提交）。1 万个线程就是几十 GB 的地址空间预留。
2. **创建和切换**：创建一个线程约几十微秒；上下文切换需要进入内核，保存和恢复寄存器，还会污染缓存。
3. **数量上限**：操作系统、容器、用户限额都有限制。

**真实上限（本机）**：macOS 上每个进程最多 4096 个线程。让 Java 提交 5000 个各自睡眠 1 秒的任务给缓存线程池，真实结果：

```
Failed to start thread ... pthread_create failed (EAGAIN)
java.lang.OutOfMemoryError: unable to create native thread
```

Python 创建 5000 个 `threading.Thread` 同理，报 `RuntimeError: can't start new thread`。

**为什么这对服务器是问题**：如果每个请求占一个线程，而请求大部分时间在等数据库，则线程大多数时候在**睡觉**，却占着栈和调度成本。线程数决定了最大并发连接数，约几千，C10K 问题（单机一万并发连接）就是由此得名。

**要记住的一点**：线程的限制不是 CPU 算力，而是它作为“被调度的重量级实体”的成本，所以后来的所有模型都在设法让“等待”不再占一个线程。
