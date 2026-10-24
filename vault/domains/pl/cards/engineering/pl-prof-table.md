---
id: pl-prof-table
node: engineering.profiling
type: qa
step: 6
---
## Q
Go、Java、Rust、Python、C++ 各自的标配剖析工具是什么？它们选了采样还是插桩，换来什么，代价是什么？

## A
| 语言 | 标配工具与方式 | 换来 | 代价 |
|---|---|---|---|
| Go | 运行时内置采样（`runtime/pprof`），线上经 `net/http/pprof` 暴露端点；同一机制还产出堆、goroutine、阻塞、互斥锁剖析 | 开箱即用，可常开 | 只看得到 Go 运行时认识的栈；`cgo` 里的 C 代码细节少 |
| Java | JFR（JDK Flight Recorder，JVM 内置的事件记录器）；外部的 async-profiler | JFR 开销低、可持续开启，事件丰富（GC、锁、分配、I/O） | 默认采样间隔较粗；要用 JDK Mission Control 等工具阅读 |
| Rust | 无运行时，用系统工具：Linux 的 `perf`、`cargo flamegraph`、macOS 的 Instruments | 没有额外运行时开销，能看到真实机器码和硬件计数器 | 要自己配置符号与帧指针；没有语言级的统一做法，上手门槛高 |
| C++ | 同 Rust，用系统工具：`perf`（Linux）、Instruments（macOS）、VTune，以采样为主 | 无运行时开销，看到真实机器码和硬件计数器（缓存缺失、分支预测） | 要 `-g` 和保留帧指针（`-fno-omit-frame-pointer`），内联和优化让栈难读；模板符号名极长 |
| Python | `cProfile`（标准库，插桩）；`py-spy`（外部采样，从外部读进程内存） | `cProfile` 调用次数精确；`py-spy` 不改代码就能附加到运行中的进程 | `cProfile` 开销大且失真；`py-spy` 在 macOS 上通常需要管理员权限；C 扩展内部只显示为一个函数 |

**规律**：有运行时的语言（Go、Java）把剖析做进运行时，因为运行时本来就知道每个线程在跑什么；没有运行时的 Rust 和 C++ 把工作交给操作系统和 CPU；Python 解释器天然在每次调用处有钩子，所以标准库给的是插桩，要采样只能从进程外面读。这也反映了各自的哲学：Go 与 Java 想让「线上随时看一眼」成为日常，Rust 的重点是零成本，不替你内置运行时设施。
