---
id: pl-foundations-execution-models-unique-jit
node: foundations.execution-models
type: qa
step: 4
---
## Q
Java 的「编译」为什么分成 `javac` 和 JVM 两个阶段？这和 Go、Rust 的一次性编译相比，给 Java 带来了什么独有的能力？

## A
`javac` 只做一件事：把 `.java` 编译成与 CPU 无关的 `.class` 字节码，并做类型检查。机器码是 JVM 在程序运行过程中，根据真实运行数据再生成的。

这带来三个独有的能力：

1. 一次编译处处运行：同一个 `.class` 可以在 x86 的 Linux 和 ARM 的 Mac 上跑，只要有对应的 JVM。
2. 按运行时事实优化：JIT 可以观察到某个接口调用其实 99% 指向同一个实现类，就把虚调用直接内联；一旦新类被加载、假设失效，就「去优化」回解释器重编。提前编译的 Go 和 Rust 看不到这些信息。
3. 代码随时间变快：热点方法会被重新编译成更优的版本，长时间运行的服务可以比刚启动时快。

代价也是这一结构带来的：启动时先解释，要经历预热期，内存里还要放着 JIT 编译器和 profile 数据。Go 和 Rust 的程序第一毫秒和第一小时速度一样，Java 的程序要「热起来」。实际对比：`hello world` 约 24 ms 才结束，而原生程序约 2 ms。
