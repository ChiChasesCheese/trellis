---
id: pl-conc-structured-evolution
node: concurrency.structured-concurrency
type: qa
step: 11
---
## Q
结构化并发的想法是怎么形成并扩散到各语言的？

## A
**思想来源**：Martin Sústrik 在 2016 年为 C 库 libdill 提出“结构化并发”一词；Nathaniel J. Smith 在 2018 年的文章《Notes on structured concurrency, or: Go statement considered harmful》中系统论证了 `go` 语句与 `goto` 的同构问题，并在 Python 的 Trio 库里实现了 nursery（托儿所：子任务只能在 nursery 里出生，nursery 不关闭就不退出）。同期 Roman Elizarov 把它带入 Kotlin 协程（`coroutineScope`）。

**扩散**：
- Kotlin：协程作用域与 `launch` 默认就是结构化的；
- Swift：5.5（2021）的 `async let` 与任务组；
- Java：Project Loom 把它做成 `StructuredTaskScope`，JDK 19 孵化、JDK 21 起多轮预览，JDK 25 仍是预览特性，API 在迭代中；
- Python：3.11（2022）把 Trio 的思路带入标准库 `asyncio.TaskGroup`，同时引入 `ExceptionGroup` 和 `except*`；
- Rust：`std::thread::scope` 在 1.63（2022）稳定，起源于 crossbeam 的 scoped threads；tokio 提供 `JoinSet`；
- Go：`errgroup` 是库约定，语言本身没有计划改变 `go` 语句。

**趋势**：
1. 与轻量并发（虚拟线程、协程）配套：任务变便宜之后，“管理它们的生命周期”成为主要问题，结构化并发是答案。
2. 取消和错误传播被视为一等公民，而非事后补丁，类似异常处理从 `setjmp` 演化到 `try/finally`。
3. 非结构化的启动方式不会消失，但被标为“逃生舱”（需要明确的理由和主人）。
