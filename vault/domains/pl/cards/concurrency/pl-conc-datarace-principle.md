---
id: pl-conc-datarace-principle
node: concurrency.data-race-freedom
type: qa
step: 1
---
## Q
什么是数据竞争（data race）？它和更宽泛的竞态条件（race condition）有什么区别？语言有哪些办法预防或发现它？

## A
**数据竞争**有一个精确的定义，三个条件同时成立：
1. 两个或更多线程访问**同一个内存位置**；
2. 其中至少一个是**写**；
3. 它们之间没有同步（锁、原子操作、通道等建立 happens-before）。

数据竞争的后果比「结果不对」更糟：在 C++ 和 Rust 的 `unsafe` 里是未定义行为（编译器可以假设它不发生）；在 Java 和 Go 里语义虽被限制，但读到撕裂的值、看不到更新、数据结构被破坏（哈希表扩容中途被读）都可能发生。

**竞态条件**是更宽的概念：结果取决于线程交错的时机。典型是「检查-再-操作」（check-then-act）：每一步各自被锁保护，但两步之间状态被别的线程改了。**没有数据竞争的程序仍然可能有竞态条件**。

**语言的四种应对策略**：
1. **编译期禁止**：类型系统规定什么能跨线程、谁能同时修改。Rust 的 `Send`/`Sync` 与借用检查。
2. **运行期检测**：插桩记录每次内存访问，发现无同步的冲突访问就报告。Go 的 `-race`、C/C++/Rust 的 ThreadSanitizer。
3. **运行期安全网**：容器在检测到并发修改时快速失败。Go 的 `fatal error: concurrent map writes`、Java 的 `ConcurrentModificationException`。
4. **靠纪律和约定**：不可变对象、线程封闭、文档标注线程安全性。Java 与 Python 的主要手段。

策略越靠前，bug 越早暴露，对语言的约束也越多。
