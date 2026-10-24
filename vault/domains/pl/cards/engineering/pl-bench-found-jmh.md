---
id: pl-bench-found-jmh
node: engineering.benchmarking
type: qa
step: 3
---
## Q
JMH（Java Microbenchmark Harness）是什么？它为什么要预热、为什么每组测量都新开一个 JVM、为什么要求基准方法返回结果？

## A
JMH 是 OpenJDK 项目维护的基准框架。用注解声明：`@Benchmark` 标记被测方法，`@State` 声明保存输入的对象，`@Warmup` 与 `@Measurement` 指定预热和测量的轮数，`@Fork` 指定重复启动多少个新 JVM。编译时由注解处理器生成包装代码，运行时由 JMH 驱动。

它防的坑与对应机制：
- **预热**（warmup）：JVM 先解释执行，热点方法逐步被 JIT 编译，速度会变。预热轮只运行、不计入结果，测量只取稳态。
- **每个 fork 是一个全新的 JVM**：上一个基准留下的运行时画像（例如某个虚方法调用点已经见过多种类型）会影响后一个的编译结果。独立进程让每次测量从干净的状态开始，也让几次 fork 的差异暴露出来。
- **返回值与 `Blackhole`**：JMH 会消费方法的返回值（或你显式传入的 `Blackhole`），所以 JIT 不能认定「结果没人用」而删除计算。
- **输入放在 `@State` 字段里**，不要写成字面量，否则常量折叠会让计算在编译期完成。

**一个实际的坑**：新版 JDK（本机为 25）的 `javac` 默认不再运行 classpath 上的注解处理器，JMH 与 jcstress 这类项目必须在编译参数里加 `-proc:full`。漏了这一步，运行时会报找不到 `META-INF/BenchmarkList`，而不是编译错误。
