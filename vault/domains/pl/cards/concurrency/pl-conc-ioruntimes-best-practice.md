---
id: pl-conc-ioruntimes-best-practice
node: concurrency.io-runtimes
type: qa
step: 9
---
## Q
在四种运行时里写网络服务，资深工程师各自应该遵守哪些规则，才能让 I/O 并发既高效又不出事故？

## A
**通用规则**：每个网络调用都有超时；限制并发（连接数、队列长度）；CPU 密集和阻塞调用不放进 I/O 线程；优雅关闭。

**Go**：
- 用 `net/http` 的标准服务器；设置 `ReadHeaderTimeout`、`IdleTimeout`；客户端用带 `Timeout` 的 `http.Client`，或每次请求传带截止时间的 `context`。
- 对自己的 `net.Conn` 使用 `SetReadDeadline`/`SetWriteDeadline`，否则 goroutine 会永远停在 `Read` 上。
- 一个 goroutine 一个连接没问题，但要用 `errgroup` 或 `WaitGroup` 管理生命周期，用 `context` 传播取消。

**Java**：
- JDK 21+ 的 I/O 密集服务，用 `Executors.newVirtualThreadPerTaskExecutor()`，不要池化虚拟线程；用 `Semaphore` 限流（限制对下游的并发，而不是限制线程数）。
- 避免在 `synchronized` 或原生方法中长时间阻塞（会钉住载体线程，JDK 24 起 `synchronized` 的钉住已基本解决）；用 `ReentrantLock`。
- 需要极致吞吐或已有 Netty 协议栈时，Netty 仍然成立。

**Rust**：
- 选 tokio 作为默认；一个 `async fn` 里不要有长时间不 `.await` 的代码，CPU 重活用 `spawn_blocking` 或 `rayon`；
- 用 `tokio::time::timeout` 包裹每个外部调用；`select!` 里留意取消安全；
- 同步的 `std::sync::Mutex` 不要跨 `.await` 持有；
- 用 `tokio-console` 观察卡住的任务。

**Python**：
- 全链路异步：用 `aiohttp`、`httpx.AsyncClient`、异步数据库驱动；同步库放进 `asyncio.to_thread`。
- 用 `asyncio.timeout()`（3.11+）、`TaskGroup` 管理生命周期；生产环境用 `uvloop` 和多进程（每个核一个进程）。
- 打开 `PYTHONASYNCIODEBUG` 或调试模式，找出占用循环超过 100 毫秒的回调。

**何时打破**：并发连接小于几百时，同步框架（Flask + gunicorn 多线程、Spring MVC）完全够用，且更容易调试和招聘人手。
