---
id: pl-conc-ioruntimes-mechanism-files
node: concurrency.io-runtimes
type: qa
step: 6
---
## Q
为什么这些运行时遇到“读文件”就得换一套办法？Go、tokio、asyncio、虚拟线程分别怎样处理不能被 `epoll` 轮询的阻塞调用？

## A
`epoll`/`kqueue` 只对“可能一直等对方”的 fd 有意义：套接字、管道、终端。**普通文件永远被认为是就绪的**（实测 macOS 的 `selectors` 对普通文件立刻返回可读；Linux 的 `epoll` 干脆拒绝注册普通文件），而真正的读盘仍然会让线程睡眠。因此磁盘 I/O、DNS 解析（`getaddrinfo`）、某些 C 库调用，不能靠“非阻塞加通知”实现，只能让**某个线程替你去阻塞**。四个运行时的做法：

| 运行时 | 阻塞调用的处理 |
|---|---|
| Go | 照常在 goroutine 里调用阻塞的系统调用；陷进内核的线程被运行时发现后，把 P（执行权）交给另一个线程，必要时新建 OS 线程 |
| Java 虚拟线程 | 文件读写会占住载体线程；JDK 临时增加载体线程补偿，避免所有虚拟线程被卡住 |
| Rust tokio | `tokio::fs` 把调用交给独立的阻塞线程池（`spawn_blocking`，默认上限 512 个线程）；自己的阻塞代码也应当这样放 |
| Python asyncio | `await asyncio.to_thread(f)` 或 `loop.run_in_executor`，交给线程池 |

asyncio 的实测：
```python
name = await asyncio.to_thread(lambda: threading.current_thread().name)
# file read runs on thread: asyncio_0 | main thread: MainThread
```
阻塞调用被放到了名为 `asyncio_0` 的池线程上，事件循环线程 `MainThread` 没被占用。

**两种思路的区别**：Go 与 Java 让**运行时**识别并补偿阻塞，用户代码不用改；Rust 与 Python 要求**用户**自己（或库作者）决定把阻塞放进哪个线程池，换来的是明确性：你知道什么在循环线程上，什么不在。

**共同的后果**：线程池有上限（tokio 的 512、Python 默认约 `min(32, cpu+4)`）。池被占满后，新的阻塞调用开始排队，表现为服务整体变慢而 CPU 并不高。排查时看线程池的排队长度，而不是事件循环。
