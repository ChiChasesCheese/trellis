# 从懂语言到精通语言：四个动手项目

卡片让你认得、说得出每个语言特性的道理；精通要靠把这些道理亲手做出来。下面四个项目按回报从高到低排列，每个都写清楚做什么、做完能检验什么、大约花多久。顺序可以调，但第 1 个最值得先做。

## 1. 自己实现一门小语言（约 4–6 周业余时间）

**做什么**：先写一个树遍历解释器（tree-walking interpreter），再把它改写成字节码虚拟机（bytecode VM），最后给虚拟机加上标记-清除 GC。语言本身很小：变量、函数、闭包、类、控制流。

**为什么回报最高**：作用域、闭包捕获、调用栈、字节码、分派、GC 这些卡片上的概念，在这个项目里全部要你亲手实现。实现过一次之后，读任何语言的运行时都能看懂它在解决什么问题。

**做完能检验**：
- 闭包为什么需要“上值”（upvalue），以及循环变量捕获的陷阱从哪里来
- 字节码解释器比树遍历快在哪里（指令分派、局部性）
- GC 的根（root）有哪些，漏掉一个根会发生什么

**语言选择**：解释器用 Java 写，虚拟机用 Rust 或 C 写（需要自己管内存才能写 GC）。

## 2. 同一个程序用四门语言各写一遍（约 2–3 周）

**做什么**：一个带持久化的并发键值存储。要求：TCP 文本协议（`GET`/`SET`/`DEL`）、多客户端并发、写前日志（WAL）、重启后从日志恢复、一个后台压缩任务。四门语言各写一版，功能相同。

**比较什么**（每项写一行结论）：
- 代码行数与写完所需的时间
- 并发模型：goroutine、虚拟线程、tokio、asyncio 各自怎么写，哪里最别扭
- 错误处理：I/O 错误在四个版本里分别怎样传播
- 内存与尾延迟：用同一个压测脚本测 p50 / p99 / 内存峰值
- 出 bug 的方式：哪个版本最容易写出数据竞争或资源泄漏

**做完能检验**：每门语言的设计哲学在一个真实系统里是怎样体现、又怎样限制你的。

## 3. 读规范与运行时源码（持续，每周 2–3 小时）

| 读什么 | 重点 |
|---|---|
| Go 语言规范（全文很短） | 类型、方法集、接口、求值顺序；读完能回答所有“Go 为什么这样”的语法问题 |
| Java 语言规范第 17 章 | happens-before、final 字段语义、数据竞争的定义 |
| Rust 的 Nomicon | `unsafe` 的边界、别名规则、`Send`/`Sync` 的真正含义 |
| Go 调度器 `runtime/proc.go` | G、M、P 三者怎样配合，goroutine 阻塞时发生什么 |
| CPython 求值循环 `Python/ceval.c` 与 `bytecodes.c` | 一条字节码怎样被执行，特化指令长什么样 |

读法：带着一个具体问题去读（例如“channel 满了以后发送方去哪里了”），找到答案就停，不要从头读到尾。

## 4. 测量驱动的性能练习（每次半天）

挑一个卡片里的性能结论（例如“`List<Integer>` 比 `int[]` 慢一个数量级”“动态分派阻止内联”），用该语言的基准工具（JMH、criterion、`go test -bench`、pyperf）复现，再用剖析器（async-profiler、perf、pprof、py-spy）解释差距来自哪里。写下：预期、实测、解释、和卡片说法的出入。

**做完能检验**：你能区分“我以为”和“我测过”，这正是资深工程师和中级工程师的分界。

## 延伸阅读

- Crafting Interpreters（免费在线）：https://craftinginterpreters.com/
- The Go Programming Language Specification：https://go.dev/ref/spec
- The Rustonomicon：https://doc.rust-lang.org/nomicon/
- Java Language Specification, Chapter 17：https://docs.oracle.com/javase/specs/jls/se21/html/jls-17.html
