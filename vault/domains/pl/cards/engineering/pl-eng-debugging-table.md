---
id: pl-eng-debugging-table
node: engineering.debugging
type: qa
step: 7
---
## Q
Go、Java、Rust、Python、C++ 在线上排障时，各自“不重启就能拿到”的东西有哪些？

## A
| 语言 | 看线程/协程 | 看内存 | 内置的低开销观测 | 主要弱点 |
|---|---|---|---|---|
| Go | `SIGQUIT`、`/debug/pprof/goroutine?debug=2` | `pprof` heap profile | `net/http/pprof`、`runtime/trace`、`expvar`，一行代码引入 | 没有堆转储可查引用链；需要事先引入 pprof 端点 |
| Java | `jcmd Thread.print`、`jstack` | `GC.class_histogram`、`GC.heap_dump` | JFR（Java Flight Recorder，常开）、JMX、`jcmd` 附加（无需重启） | 堆转储可能长暂停；信息太多需要工具 |
| Rust | `lldb`/`gdb` 附加；`async` 任务用 `tokio-console` | `heaptrack`、`dhat`、`valgrind` | `tracing` 加 `tokio-console`；崩溃时 `RUST_BACKTRACE` | 没有运行时自省，要靠事先埋点；符号与泛型名难读 |
| Python | `faulthandler`、`py-spy dump`（外部读内存） | `tracemalloc`（需事先开启）、`objgraph` | `py-spy`、`sys.settrace`（开销大） | 默认不开 `tracemalloc`，事后补不了；多进程分散 |
| C++ | `gdb`/`lldb` 附加，`thread apply all bt`；崩溃留下核心转储（core dump） | `heaptrack`、Valgrind、ASan/LeakSanitizer；分配器自带的堆统计 | `perf`、eBPF、`ltrace`；崩溃时的核心转储与信号处理 | 没有运行时自省；发布构建的优化和内联让栈和变量面目全非；需要 `-g` 符号与独立的调试信息文件 |

逻辑：
- **Java** 能做得最全，因为 JVM 拥有完整的运行时：线程、堆、类型信息、JIT 都在它手里，所以附加接口（Attach API）和事件系统（JFR）可以做到深入且低开销。
- **Go** 的运行时也能自省，但风格是“把观测端点编进程序里”（pprof 端点），相信工程师会提前引入。
- **Rust** 没有运行时可问，一切观测都要通过外部工具读取原生进程或靠程序主动输出。它把力气放在“让 bug 在编译期就出现不了”上，而不是出事后好调。
- **C++** 与 Rust 同属“没有运行时可问”，但崩溃的形态不同：段错误是未定义行为的后果，进程直接死掉，唯一的现场是核心转储，所以 C++ 的排障文化是“带符号发布 + 核心转储 + 调试器”。这是零开销原则的直接结果：运行时不为你保留自省信息。
- **Python** 的解释器暴露了大量内省手段，但默认不记录历史（比如分配栈），出事后无从追溯。

要点：排障能力是**平台在设计时留下的接口**；一旦进入线上，缺什么都已经补不了。
