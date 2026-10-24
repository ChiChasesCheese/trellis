---
nodes: [runtime.jit, runtime.performance-model, runtime.compiler-pipeline, runtime.startup-footprint]
tags: [drill]
---
# 练习：刚发布的 Java 实例前几个请求特别慢，而 Rust 版本比 Java 还慢

一个 Java 服务每次发布后，前几秒的 p99 是平时的几十倍，之后恢复正常。同一周，另一位同事把 Rust 重写版和 Java 版放在一起跑了个循环基准，Rust 慢了近 10 倍，他的结论是「Java 比 Rust 快」。你要解释两个现象，并给出上线前的预热方案。

同一台机器上，一个包含 `HashMap` 合并、流式排序和 `String.format` 的请求处理函数，在同一个 JVM 里连续调用，单次耗时依次是：

| 第几次调用 | 耗时（微秒） |
|---|---|
| 1 | 10991 |
| 2 | 69 |
| 10 | 55 |
| 100 | 20 |
| 1000 | 3 |
| 10000 | 2 |

加上 `-Xint`（只解释执行，不做 JIT）后，稳态单次耗时约 65 微秒。另有一个一亿次迭代的纯 CPU 循环（`s += i*i % 7`）：Java 约 28 ms，Go 约 37 ms，Rust `-O` 约 32 ms，Rust 不加优化（debug 构建）约 291 ms，CPython 约 2246 ms。

**要你给出的**
- 表中第 1 次、第 2 次到第 100 次、第 1000 次以后的耗时分别花在哪里（类加载、解释执行、JIT 编译、编译后的代码）。
- 对「Java 比 Rust 快」这个结论的反驳：哪里测错了，应该怎样重测。
- 一份上线预热方案，以及 Go、Rust、Python 是否有同样的问题。
- 把五个循环结果按量级分成三档，并说明每一档的机制。

**评分要点**
- 第 1 次约 11 ms：首次执行要加载类、解析常量池、绑定 lambda 和 `String.format` 的内部类，字节码此时还在解释器里跑。第 2 次到第 100 次降到几十微秒：类已加载，但仍主要是解释执行加上分层编译的第一层（C1）。第 1000 次以后到 2 到 3 微秒：热点方法被 C2 编译成优化后的机器码，并内联了调用链 ([[pl-rt-jit-found-hotspot-tiers]], [[pl-rt-jit-found-basics]])。
- `-Xint` 稳态约 65 微秒，稳态编译后约 2 到 3 微秒，差约 30 倍，这就是 JIT 买到的东西；代价是启动阶段的慢和额外的编译线程、内存 ([[pl-rt-jit-mechanism-speculation]], [[pl-rt-jit-principle]])。
- 「Java 比 Rust 快」的反驳：被比较的是 Rust 的 debug 构建（约 291 ms），而不是 `-O` 的 release 构建（约 32 ms）；release 与 Java 在同一量级。debug 构建关掉了内联、向量化和大部分优化，只用于开发。重测要在 release 构建下，用 `black_box` 防止编译器把循环优化掉，并多次运行取稳态 ([[pl-rt-compiler-pitfall-debug-build]], [[pl-rt-opt-pitfall-dce-benchmark]])。
- 三档：Rust `-O`、Java（预热后）、Go 在 30 到 40 ms，是编译成机器码并优化过的；Rust debug 约 290 ms，是没有优化的机器码；CPython 约 2246 ms，约为 Rust release 的 70 倍，每次迭代都要解释字节码、创建整数对象并做类型分派 ([[pl-rt-perf-mechanism-ladder]], [[pl-rt-perf-found-boxing]])。
- 预热方案：发布后先用回放流量或合成请求走一遍关键路径，等到接口延迟稳定才让就绪探针通过；使用应用类数据共享（AppCDS）缩短类加载；滚动发布时让新实例先接小比例流量；监控要把发布后的前几分钟单独看，不混进稳态 p99 ([[pl-rt-jit-pitfall-warmup]], [[pl-rt-startup-found-jvm]])。
- Go 与 Rust 是提前编译，没有运行时预热，启动即稳态（Go 的 hello world 启动约 2 ms，Rust 约 1.5 ms）；CPython 同样没有 JIT 预热，慢是恒定的慢，而不是启动期的慢；如果是 Python 想要 JIT，要换实现（PyPy 的追踪 JIT 同样有预热） ([[pl-rt-startup-table]], [[pl-rt-jit-found-tracing-pypy]])。
- 基准测试的共同纪律：区分启动、预热与稳态，三者分开测、分开报告 ([[pl-bench-pitfall-warmup]], [[pl-bench-philosophy-jit-vs-aot]])。

**练习记录**
- [ ] 第 1 次（日期、用时、自评）：
