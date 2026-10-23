---
id: hl-javaq-c-q07-table
node: java-questions.c-languages
type: qa
step: 2
---
## Q
从类型、执行、内存管理、并发四个维度对比 Java 与 CPython。

## A
- **类型**：Java 静态，编译期检查，泛型被擦除；Python 动态，类型注解不强制。
- **执行**：Java 字节码 + JIT（C1/C2），稳态接近本地代码；CPython 字节码解释（3.13 有实验 JIT），纯 Python 循环通常比 Java 慢**一到两个数量级**。
- **内存管理**：Java 是追踪式 GC（可达性），互相引用的循环对象也能回收；Python 是引用计数 + 循环垃圾收集器，`__del__` 时机较确定。
- **并发**：Java 是真线程（OS 线程），共享内存 + Java 内存模型（JMM），还有虚拟线程；Python 有 **GIL**，同一时刻只有一个线程执行字节码，CPU 密集要多进程；3.13 有 free-threaded 实验构建。
- **启动 / 内存**：JVM 启动百毫秒级、内存占用大；Python 启动快、占用小。
