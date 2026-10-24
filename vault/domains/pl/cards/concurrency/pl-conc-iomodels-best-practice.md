---
id: pl-conc-iomodels-best-practice
node: concurrency.io-models
type: qa
step: 8
---
## Q
设计网络服务时，资深工程师怎样选择 I/O 模型，并避免常见的 I/O 相关的生产事故？

## A
**选型**：
1. **别自己写事件循环**。使用语言的标准运行时或成熟框架（Go 标准库、Netty、tokio、asyncio / uvicorn），它们已经处理了就绪语义、公平性、关闭与缓冲区问题。
2. **能用阻塞风格就用阻塞风格**：Go 默认如此；Java 21+ 选虚拟线程（每个请求一个）；服务大部分时间在等下游时，这是最简单且可维护的办法。
3. **Rust 和 Python 需要异步时**：整个调用链都用异步库，不在 `async` 里混用阻塞调用。
4. **CPU 密集的工作不属于 I/O 模型**：单独的线程池或进程池，不要放进事件循环线程。

**必须配置的三样东西**（任何模型下都一样）：
- **超时**：连接超时、读写超时、整体请求截止时间（Go 的 `context` 和 `http.Server` 超时，Java 的 `HttpClient.timeout`，tokio 的 `timeout`，asyncio 的 `wait_for`）。没有超时的网络调用迟早会让你的连接池被一个卡住的下游耗尽。
- **限流与背压**（backpressure）：限制并发数和排队长度；读得比写得快，缓冲区会无限增长。
- **优雅关闭**：停止接收新连接，等进行中的请求做完或超时，再退出。

**注意文件 I/O 不是网络 I/O**：普通文件对 `epoll`/`kqueue` 永远“就绪”（实测 macOS 上 `selectors` 对普通文件立即返回就绪；Linux 的 `epoll` 甚至直接拒绝注册普通文件），所以磁盘读写在 Go 的运行时、tokio（`tokio::fs`）、asyncio（`run_in_executor`）、Java NIO 里最终都是由线程池里的阻塞调用完成的。需要真正的异步磁盘 I/O，才考虑 `io_uring`。

**监控**：看活跃连接数、事件循环延迟（Python 的 loop lag、tokio 的 task poll 时间）、线程池排队长度，而不是 CPU 百分比。

**何时打破**：连接数小于几百、延迟要求不苛刻时，简单的线程池加阻塞 I/O 完全足够，别为了“高并发”引入不必要的复杂度。
