---
nodes: [concurrency.choosing, concurrency.gil, concurrency.executors, concurrency.locks-races, concurrency.multiprocessing]
tags: [drill, interview]
---
# Drill：三个任务，各选线程/进程/asyncio 并说代价

三个独立任务，各自要给出「用线程池、进程池还是 asyncio」的结论和理由：

1. 拉取 500 个 URL（用同步的 `requests` 库，无 async 版本可用）。
2. 解析一份 5 GB 的 CSV，做纯 Python 的分组聚合。
3. 反复调用一个会释放 GIL 的 NumPy 数值内核（如大矩阵乘法），调用次数很多但每次纯计算、不涉及 I/O。

**限制与要求**
- 每个任务先给结论（线程/进程/asyncio 三选一），再说代价，不许颠倒顺序。
- 必须提到 GIL 在这个任务里到底释放不释放，这是决定结论的核心依据。
- 不许只说「因为 I/O 密集用线程」这种套话，要说出为什么这个具体任务符合或不符合该模式。
- 3 分钟一个任务，超时就先给结论再补理由。

**分关要求**
- 第 1 关：给出三个任务各自的结论 + 一句话理由。
- 第 2 关：追问——如果任务 1 里的某个 URL 请求返回后要用一个共享的 `dict` 累计各 URL 的状态码计数（`counts[code] += 1`），这行代码在多线程下安全吗？
- 第 3 关：追问——如果把任务 2 从多线程改成多进程，父进程本身还开着其他后台线程（比如一个日志上报线程），在 Linux 上直接用默认 `fork` 起子进程有什么风险？3.14 起默认行为变了什么？

**评分点（强答案会命中）**
- 选型一句话结论：I/O 密集看依赖库是否阻塞——阻塞库用线程，有 async 版本且要支撑高并发连接数用 asyncio；CPU 密集的纯 Python 计算用进程绕开 GIL，或者换成释放 GIL 的 C 实现（NumPy/DuckDB） [[choosing-decision-tree-main]]
- 三种方案各自的代价：线程仍共享 GIL、CPU 密集无法真正加速、共享状态要显式加锁；进程有独立内存空间，参数返回值要走 pickle，跨进程通信有额外开销；asyncio 单线程协作式调度，一旦某个协程同步阻塞或纯 CPU 计算不让出控制权，会卡住整条事件循环上所有任务 [[choosing-cost-per-option]]
- 同步阻塞库（没有 async 版本）没法用 asyncio，因为一次同步阻塞调用会卡住单线程事件循环上的所有并发任务；这时线程池是更现实的选择，哪怕效率不如原生 asyncio [[choosing-threads-vs-asyncio-io]]
- CPU 密集型纯 Python 任务加多线程反而更慢：线程几乎不会主动释放 GIL，本质仍是靠切换间隔强制轮流串行执行字节码，额外的线程创建/切换/GIL 争用开销纯属浪费 [[choosing-thread-cpu-bound-slower]]
- GIL 在阻塞式系统调用前会被主动释放（I/O 等待期间其他线程可执行），C 扩展在纯 C 计算区域也可以显式释放（NumPy 数值内核就是这种情况），只在需要操作 Python 对象时才重新获取 [[gil-who-releases]]
- 同一进程内所有线程共享同一把 GIL，多线程跑纯 Python 计算不会有并行加速；多进程各自独立解释器和 GIL，能真正利用多核，代价是参数返回值必须可 pickle [[gil-vs-multiprocessing]] [[mp-bypasses-gil-needs-pickle]]
- `counts[code] += 1` 不是原子操作：GIL 只保证解释器内部状态（如单个字节码指令）的原子性，不保证一整条复合语句的原子性，`+=` 会被编译成多条字节码，线程可能在中间被切换出去导致丢更新，仍需要显式加锁或用线程安全的容器（如 `collections.Counter` 配合锁，或每线程本地计数再汇总） [[gil-not-your-data]]
- `fork` 只复制发起 `os.fork()` 的那一个线程，父进程其他线程持有的锁状态不会被正确复制，容易在子进程里死锁；3.14 起 POSIX 平台默认启动方式从 `fork` 改成 `forkserver`，由一个专门的单线程服务进程去 fork，兼顾速度和安全（Windows/macOS 默认仍是 `spawn`） [[mp-start-methods-tradeoff]] [[mp-314-default-forkserver]]

**参考答案**
1. 拉 500 个 URL：选线程池（`ThreadPoolExecutor`）。`requests` 是同步阻塞库没有 async 版本，asyncio 用不上；这是纯 I/O 等待，线程在发起网络调用前会释放 GIL，500 个线程（或更现实地设置 max_workers 做限流）足以把等待时间重叠起来，不需要多进程的独立内存和 pickle 开销。
2. 解析 5 GB CSV 做纯 Python 聚合：选进程池（`ProcessPoolExecutor`），把文件分块、每个进程处理一块再合并结果。纯 Python 计算几乎不释放 GIL，多线程等于串行执行还多花调度开销；多进程的代价是分块结果要能 pickle（通常是小的聚合字典，代价可接受）。如果允许换实现，用 pandas/DuckDB 向量化聚合往往比手工分进程更快。
3. 反复调用释放 GIL 的 NumPy 内核：选线程池而不是进程池。虽然是 CPU 密集，但因为内核本身在纯 C 计算区域显式释放了 GIL，多个线程可以真正并行跑在多个核心上，不需要付出进程间通信和序列化大数组的代价；只有当调用的库不释放 GIL 时才需要退回多进程。

第 2 关：不安全。`counts[code] += 1` 展开为读取-加一-写回三步字节码，多线程下可能在中间被切换，导致丢更新；即使 GIL 存在也不保证这条复合语句整体原子，需要显式加锁或改成每线程本地计数最后汇总。

第 3 关：默认 `fork` 只复制发起 fork 的那个线程，父进程里的日志上报线程如果当时正持有某把锁，子进程里这把锁会永远处于「已加锁」状态却没有对应线程去释放，容易造成子进程死锁或挂起；3.14 起 POSIX 默认改成 `forkserver`，由一个专门维护的单线程服务进程去做实际的 fork，避免对多线程父进程直接 fork 的隐患，同时仍比 `spawn` 快。

**尝试记录**
| 日期 | 用时 | 卡在哪 | 下次 |
|---|---|---|---|
