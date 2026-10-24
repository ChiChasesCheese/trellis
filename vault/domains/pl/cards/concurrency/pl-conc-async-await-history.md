---
id: pl-conc-async-await-history
node: concurrency.async-await
type: qa
step: 9
---
## Q
`async/await` 这个语法是从哪里来的？它在 Python、Rust、Java 里分别是什么时候出现的，现在的趋势是什么？

## A
**来源**：C# 5.0（2012）把 `async/await` 带入主流语言，思路是让编译器把顺序写法改写成状态机，来代替回调。之后 Python、JavaScript（ES2017）、Rust、Kotlin、Swift 都采用了同样的关键字。

**各语言的时间线**：
- Python：3.4（2014）标准库加入 `asyncio`，用 `yield from` 写协程；3.5（2015）引入 `async def` 与 `await` 关键字（PEP 492）；之后 `asyncio.run`、`TaskGroup`（3.11）等不断补齐。
- Rust：1.39（2019 年底）稳定 `async/await`；运行时一直留给 tokio 等库，标准库只有 `Future`。
- Java：没有加这对关键字。Java 8 的 `CompletableFuture` 提供链式异步；Java 21（2023）的虚拟线程正式发布，路线是让阻塞写法重新变得可行。
- Go：一开始就没有，goroutine 就是答案。
- C++：C++20（2020）加入协程（`co_await` 等关键字），同样是编译器改写成无栈状态机，但标准库不带任务类型和调度器，C++26 的 `std::execution` 才补上调度框架。

**趋势**：`async/await` 解决了回调地狱，但留下函数着色、生态分裂（同步、异步两套库）、取消语义难做对的代价。新一代方案（虚拟线程、结构化并发）想保留顺序写法的简单，同时拿到轻量并发。两条路线今天并存：需要极小内存占用、无运行时（嵌入式、内核）的场景仍然偏爱 Rust 式状态机，通用服务端则越来越倾向便宜线程。
