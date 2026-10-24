---
id: pl-fuzz-found-jazzer-atheris
node: engineering.fuzzing
type: qa
step: 5
---
## Q
Java 的 Jazzer 和 Python 的 Atheris 是怎样做覆盖率引导模糊测试的？在虚拟机语言里「崩溃」指什么？

## A
两者都以 libFuzzer 为引擎，区别在于怎样拿到「覆盖了哪些分支」：

- **Jazzer**（Java/JVM）：用 Java agent 在类加载时对**字节码**插桩，向 libFuzzer 报告执行到的边。fuzz 目标是一个接受 `byte[]` 或 `FuzzedDataProvider` 的方法；也可以用 JUnit 5 集成（`@FuzzTest`），让模糊测试成为测试套件的一部分。除了崩溃，它内置了针对 Java 常见漏洞的检测器：反序列化、SQL 注入、命令注入、路径穿越等。
- **Atheris**（Python）：对 Python **字节码**插桩（`atheris.instrument_imports()`），同样由 libFuzzer 驱动。也可以与 AddressSanitizer 一起使用，去模糊测试 C 扩展里的内存错误。注意：它依赖带有 libFuzzer 的 LLVM Clang，在 macOS 自带的 Apple Clang 上安装会失败（本机实测报错 `Failed to find libFuzzer`），需要先装官方 LLVM。

**在虚拟机语言里，「崩溃」是什么**：JVM 和 CPython 的内存是安全的，很少出现段错误。常见的失败信号是**未捕获的异常**：Java 的 `NullPointerException`、`ArrayIndexOutOfBoundsException`、栈溢出、`OutOfMemoryError`，Python 的未处理异常、递归过深。这意味着：
- 抛出被**预期**的异常（比如解析失败抛 `ParseException`）不算 bug，fuzz 目标里必须 `catch` 住，只让「不该出现的异常」逃出去；
- 找到的往往是逻辑错误和拒绝服务（超时、内存耗尽、算法复杂度爆炸、正则回溯），而不是内存破坏。
