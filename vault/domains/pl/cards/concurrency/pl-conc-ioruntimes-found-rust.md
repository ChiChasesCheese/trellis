---
id: pl-conc-ioruntimes-found-rust
node: concurrency.io-runtimes
type: qa
step: 4
---
## Q
Rust 的 mio 和 tokio 是什么关系？tokio 的 `TcpStream::read().await` 在“读不到数据”时具体发生了什么？

## A
Rust 标准库只有阻塞的网络 API 和 `Future` 抽象，没有事件循环。事件循环由库提供：
- **mio**：对 `epoll`/`kqueue`/IOCP 的薄包装。核心是三个对象：`Poll`（等待）、`Registry`（把 fd 注册为某个 `Token` 并声明关心的事件）、`Events`（返回就绪的结果）。
- **tokio**：在 mio 之上加了**执行器**（多线程的任务调度器）、**I/O 驱动**（接收 mio 的事件并唤醒任务）、定时器、异步文件与网络类型。

mio 的最小例子（一个线程睡眠在内核里，直到有人连接）：
```rust
poll.registry().register(&mut ln, Token(0), Interest::READABLE)?;
poll.poll(&mut events, None)?;                       // epoll_wait / kevent
for e in events.iter() { println!("token={:?} readable={}", e.token(), e.is_readable()); }
```
输出：`polling... (thread sleeps in the kernel)`、`event: token=Token(0) readable=true`、`accepted a connection from loopback: 127.0.0.1`。

**tokio 的 `read().await`**：
1. `TcpStream::read` 返回一个 `Future`；每次被 `poll` 时先尝试非阻塞读；
2. 读到数据就返回 `Poll::Ready`；
3. 读不到（`WouldBlock`）就把任务的 `Waker` 存进该连接的“就绪状态”，返回 `Poll::Pending`，任务让出线程；
4. I/O 驱动收到 mio 的事件，调用 `Waker`，调度器把任务放回队列，再次 `poll`。

**mio 的事件是边沿触发的**：只在状态变化时通知一次，所以 tokio 内部要在读到 `WouldBlock` 才清除就绪标志。用户通过 `.await` 看不到这些，只有手写 `poll_read` 时才会碰到。

实测（一次测量）：5000 个空闲连接，每个连接一个 tokio 任务，OS 线程固定为 13（工作线程数由核数决定），内存从 2 MB 增到 10 MB，约 1.6 KB 每连接：任务只是一个状态机对象，没有独立的栈。

**设计后果**：运行时是库，所以可以选（tokio、async-std、smol，嵌入式用 embassy）；也因此生态要和某个运行时绑定，库的 API 里常常出现 `tokio::` 类型。
