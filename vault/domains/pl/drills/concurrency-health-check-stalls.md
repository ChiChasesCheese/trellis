---
nodes: [concurrency.async-await, concurrency.green-threads, concurrency.gil, concurrency.parallelism]
tags: [drill]
---
# 练习：每次生成月度报表，健康检查的 p99 就跳到 250 毫秒

订单服务的 `/health` 平时 2 ms 返回。每当有人触发「月度报表」（纯 CPU 计算，单次约 250 ms），`/health` 的 p99 就跳到约 250 ms，负载均衡把实例摘掉。同样的逻辑被写成 Python（asyncio）、Rust（tokio 单线程运行时）、Java 25（虚拟线程，只有 1 个载体线程）和 Go 四个版本。你要把症状诊断到机制，预测四个版本各自会不会出现，并给出每个版本的正确修复。

**要你给出的**
- 症状的可能原因，按可能性从高到低排序，至少 4 条，每条写一句验证办法。
- 四个版本里，「在事件循环或调度线程上直接跑 250 ms 的 CPU 计算」会不会冻结其他任务，并说明调度器为什么能或不能把 CPU 拿回来。
- Python 的三种修复（直接调用、`asyncio.to_thread`、进程池）各自的效果，以及为什么线程不能真正解决 CPU 密集问题。
- Java 虚拟线程里「在 `synchronized` 块里睡眠」这个经典固定（pinning）问题，在 Java 25 上还存在吗？

**评分要点**
- 原因排序：先是事件循环或载体线程被 CPU 计算或同步阻塞调用占住；其次是线程池或连接池耗尽；再是 GC 停顿；再是锁竞争；最后才是网络本身。验证办法分别是：测事件循环的最大调度间隔、看线程转储、看 GC 日志、看锁等待、抓包 ([[pl-conc-async-await-pitfall-blocking]], [[pl-trends-conc-pitfall-blocking]])。
- Python（asyncio）：事件循环是单线程的协作式调度，一个协程不 `await` 就不会让出。直接调用时，循环的最大停顿等于计算时长（实测计算 240 到 250 ms，停顿 240 到 250 ms） ([[pl-conc-async-await-mechanism-loop]], [[pl-conc-async-await-principle]])。
- `asyncio.to_thread` 把计算挪到线程，停顿缩短了（同一台机器上约 85 ms），但没有消失：线程仍要和事件循环线程争抢 GIL，CPU 密集代码在线程里并不并行。进程池把停顿降到几毫秒（实测 6 到 7 ms），代价是进程间序列化数据和启动成本 ([[pl-conc-gil-found-behavior]], [[pl-conc-gil-found-escape-routes]], [[pl-conc-gil-pitfall-multiprocessing]])。
- Rust（tokio 单线程运行时）：异步任务同样是协作式的，在任务里直接循环 10 亿次，最大停顿约等于计算时长（实测计算 209 ms，停顿 209 ms）；改用 `spawn_blocking` 把计算放进专用线程，停顿降到 0 ms ([[pl-conc-async-await-found-rust-future]], [[pl-conc-async-await-best-practice]])。
- Java 25：虚拟线程不会被时间片抢占。载体线程只有 1 个时，一个 CPU 密集的虚拟线程会让别的虚拟线程等到它结束（实测计算 451 ms，另一个虚拟线程的启动延迟 435 ms）；载体线程数默认等于核数时通常看不到，直到所有载体都被占满 ([[pl-conc-green-threads-mechanism-blocking]], [[pl-conc-green-threads-found-virtual]])。
- 在 `synchronized` 里睡眠：JDK 21 会固定载体线程，JDK 24 起（JEP 491）已修复，Java 25 上同样的测试，别的虚拟线程的延迟约 1 ms，没有被拖住；仍会固定载体的情形是正在执行原生方法时阻塞 ([[pl-conc-green-threads-mechanism-blocking]], [[pl-conc-green-threads-evolution]])。
- Go：默认有多个 P（逻辑处理器），心跳 goroutine 另有处理器可用，同样的 CPU 循环实测心跳停顿 0 ms；即使只剩一个 P，调度器也会抢占长时间运行的 goroutine（异步抢占，Go 1.14 起），所以 Go 不需要「把计算移出事件循环」这条纪律，代价是失去了协作式调度的可预测性 ([[pl-conc-green-threads-unique-preempt]], [[pl-conc-green-threads-found-goroutine]])。
- 修复的共同原则：事件循环线程只做 I/O 编排；CPU 密集工作放到独立的线程池或进程池，并给它设并发上限；并监控事件循环延迟，而不是只看请求耗时 ([[pl-conc-parallel-pitfall-common-pool]], [[pl-conc-parallel-best-practice]])。

**练习记录**
- [ ] 第 1 次（日期、用时、自评）：
