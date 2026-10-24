---
id: pl-conc-async-await-table
node: concurrency.async-await
type: qa
step: 5
---
## Q
Python、Rust、Java、Go 面对「高并发 I/O」分别选了 async/await 还是别的路线？各自的代价是什么？

## A
| 语言 | 选择 | 换来 | 代价 |
|---|---|---|---|
| Python | `asyncio`：内置事件循环，3.5 起有 `async/await` | 单线程内上万并发，不需要锁，与 GIL 现实相容 | 函数着色；同步库（如 `requests`）不能直接用 |
| Rust | 语言只定义 `Future` 与 `async/await`，运行时交给 tokio 等库 | 无运行时开销，任务是小状态机，可用于嵌入式 | 函数着色，生态分裂，取消与 `Pin`/生命周期复杂 |
| Java | 没有 `async` 关键字；`CompletableFuture`，21 起首选虚拟线程 | 同步写法，无颜色，调用栈完整，调试容易 | 要等 JVM 改造；回调链（CompletableFuture）可读性差 |
| Go | 不需要，goroutine 本身就是答案 | 无颜色，一套代码 | 运行时较重，只能用 Go 运行时的调度 |

背后的逻辑：
- async/await 是「让阻塞调用便宜」做不到时的替代方案。Python 的 GIL 和 Rust 的无运行时目标，让这两门语言**不能**或**不愿**做有栈的轻量线程，只能让编译器把函数改写成状态机。
- 状态机省内存、省运行时，但把「这个函数可能挂起」写进了类型签名，代价是颜色的传染：一个底层库改成异步，所有调用者都要跟着改，库作者要同时维护两套。
- Java 和 Go 反过来：把成本放在运行时，让所有代码保持同一个颜色。两条路线是在「运行时复杂度」和「程序员/库复杂度」之间二选一，没有免费的午餐。
