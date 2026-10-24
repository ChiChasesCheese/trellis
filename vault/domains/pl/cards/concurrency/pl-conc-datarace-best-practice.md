---
id: pl-conc-datarace-best-practice
node: concurrency.data-race-freedom
type: qa
step: 8
---
## Q
不依赖 Rust 的编译器检查时，资深工程师怎样在 Java、Go、Python 里系统性地减少数据竞争？

## A
核心思路：**让共享可变状态尽可能少，并让剩下的有明确的主人。** 按成本从低到高：

1. **不可变**。不可变对象天然线程安全，可以任意共享。Java `record`、`final` 字段、`List.of`，Python `tuple`、`frozen=True` 的数据类，Go 传值而非传指针。发布时一次性完整构造，再发布引用。
2. **线程封闭**。每个线程自己的数据不共享：每个请求一份上下文、`ThreadLocal`/局部变量、Go 里“一个 goroutine 拥有这个 map，别人通过 channel 请求它”。
3. **消息传递代替共享**。把状态交给唯一的所有者，其他人发消息；数据通过通道交接后，发送方不再使用。
4. **用经过验证的线程安全容器**，而不是普通容器加手工锁：`ConcurrentHashMap`、`CopyOnWriteArrayList`、Go 的 `sync.Map`（仅适合读多写少或键不相交的场景）、`queue.Queue`。
5. **必须共享可变状态时，一把锁、一个不变量**，并把锁和数据放在同一个类里封装起来。
6. **用工具兜底，并放进 CI**：Go 的 `go test -race`，Java 的 jcstress 与静态分析（SpotBugs、Error Prone 的 `@GuardedBy` 检查），Rust 项目有 `unsafe` 就跑 Miri/loom。
7. **文档标注线程安全性**：Java 的 `@ThreadSafe`/`@GuardedBy`，Go 在注释里写“mu 保护以下字段”。让下一个人不必猜。

**判断顺序**：能不共享就不共享；共享就不可变；必须可变就单一所有者；实在要多方改，再用锁。

什么时候打破：热点路径上经过压测证明的优化，如分片锁、原子计数，需要写清论证和测试。
