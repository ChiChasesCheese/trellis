---
id: pl-trends-conc-best-practice
node: trends.concurrency-evolution
type: qa
step: 9
---
## Q
资深工程师今天怎样选择并发模型并写出可靠的并发代码？通用规则是什么，四门语言各自的做法？

## A
**通用规则**：
1. **I/O 密集用轻量并发单位，CPU 密集用与核数匹配的并行度**，二者不要混在同一个池里。
2. **每个任务有归属**：谁启动、谁等待、谁取消，用结构化并发的方式写。
3. **所有等待都有超时，所有任务都可取消**。
4. **共享可变状态最小化**：能传消息、能用不可变数据，就不用锁。
5. **限制并发度**：用信号量或有界队列做背压，别靠“资源会够用”。

按语言：
- **Go**：每个 `go` 语句要有退出条件；用 `context` 传递取消和超时；一组任务用 `errgroup`；`go test -race` 常开；限制并发用带缓冲的通道或信号量。
- **Java**：新项目在 JDK 21 以上用虚拟线程处理 I/O 型请求（`newVirtualThreadPerTaskExecutor`），不要池化虚拟线程；用 `Semaphore` 限制对下游的并发；避免在 `synchronized` 内做阻塞 I/O（会钉住载体线程），改用 `ReentrantLock`；结构化并发在稳定前可以用于内部代码并关注进展。
- **Rust**：I/O 服务用 tokio；CPU 密集的工作放进 `spawn_blocking` 或 rayon，不阻塞运行时线程；跨 `await` 持有锁要用异步锁或缩小临界区；依靠 `Send`/`Sync` 让编译器检查线程安全。
- **Python**：I/O 并发用 `asyncio` 加 `TaskGroup`；CPU 密集用 `multiprocessing` 或 `concurrent.futures.ProcessPoolExecutor`，或者原生扩展；绝不要在协程里调用阻塞函数（用 `asyncio.to_thread` 包装）；考虑 3.13 起的自由线程（free-threaded）构建，但生态兼容性需要验证。

**何时破例**：简单脚本与低并发服务，线程池足够；追求极限延迟的系统（交易、游戏）可能自己控制线程与亲和性。
