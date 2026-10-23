---
id: hft-measurement-benchmarking-dead-code
node: measurement.benchmarking
type: qa
step: 1
---
## Q
写微基准（microbenchmark）时，编译器或 JIT 的“死代码消除”和“常量折叠”会怎样破坏结果？JMH 和 Google Benchmark 怎么防？

## A
微基准是测一小段代码的耗时。优化器很聪明，可能让你测的东西根本没有执行：

- **死代码消除**（dead code elimination）：计算的结果没被任何地方使用，整段计算被删掉。你测到“0.3 ns”，其实什么都没算。
- **常量折叠**（constant folding）：输入是写死的常量，编译器在编译时就算出了答案，运行时只返回一个数。

例：循环计算 1 到 1000 的和，结果赋给一个没用到的局部变量，被整段删掉。

防范：
- **JMH**（Java Microbenchmark Harness）：让 `@Benchmark` 方法**返回**结果，或把结果交给 `Blackhole.consume()`，这样 JIT 不敢删；输入放在 `@State` 对象的字段里，使其不是常量。
- **Google Benchmark**（C++）：用 `benchmark::DoNotOptimize(x)` 告诉编译器“这个值被用到了”，用 `ClobberMemory()` 防止内存读写被省略。

检查：结果快得离谱（小于一个时钟周期）时，几乎一定是被优化掉了，需要看汇编确认。
