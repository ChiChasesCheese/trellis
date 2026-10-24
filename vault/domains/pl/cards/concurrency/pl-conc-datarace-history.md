---
id: pl-conc-datarace-history
node: concurrency.data-race-freedom
type: qa
step: 10
---
## Q
防止数据竞争的工具是怎样演化的？ThreadSanitizer、Go 的 `-race`、Rust 的 `Send`/`Sync` 各来自什么思路，趋势是什么？

## A
**思路一：运行时检测**。早期做法是 Lockset（检查每个共享变量是否总被同一把锁保护）和 happens-before 检测。Google 的 ThreadSanitizer（TSan）把它做成了可用的编译器插桩工具，随 LLVM 和 GCC 提供，覆盖 C、C++、Go；Go 在 1.1（2013）加入基于 TSan 的 `-race`，成为官方工具链的一部分，也是 Go 社区的标配（CI 里跑 `go test -race`）。Java 一侧有 jcstress 等压力测试工具。

**思路二：类型系统**。Rust 1.0（2015）把「所有权 + 借用」与 `Send`/`Sync` 结合：编译器可证明安全代码无数据竞争。这个思路建立在区域（region）与线性类型的研究之上，在 Mozilla 的 Servo 浏览器引擎项目里得到检验，口号是「无畏并发」（fearless concurrency）。

**思路三：减少共享可变状态**。不可变对象（Java `record`、Python `frozen` 数据类）、线程封闭、通道和 actor，从设计上避免共享。Erlang 与 Go 的口号都属于这一类。

**趋势**：
1. 竞争检测默认进入开发流程：Go 的 `-race`、Rust 的 Miri 与 loom（对并发代码做模型检查）、LLVM 的 TSan。
2. 其他语言也在向类型系统借力：Swift 5.5 起的 actor 与 Swift 6 的严格并发检查，都在编译期标注「什么能跨并发域」。
3. Python 的自由线程构建（3.13 起实验性）把安全性重新推到程序员手里，必须依靠锁和线程安全容器；这使这条历史线又回到起点。
