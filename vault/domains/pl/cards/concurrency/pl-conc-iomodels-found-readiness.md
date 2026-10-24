---
id: pl-conc-iomodels-found-readiness
node: concurrency.io-models
type: qa
step: 3
---
## Q
`select`、`poll`、`epoll`、`kqueue` 是什么？它们为什么能让一个线程管理上万个连接，复杂度差在哪里？

## A
它们都是**就绪通知**接口：你把一批 fd 和关心的事件（可读、可写）交给内核，然后问“哪些现在就绪了”，内核只返回就绪的那些。线程在这个调用里睡眠，直到有 fd 就绪或超时，因此既不空转，也不用一个连接占一个线程。

- **`select`**：每次调用都要把整个 fd 集合从用户态拷进内核，内核逐个扫描；集合大小有 `FD_SETSIZE`（常见 1024）上限。
- **`poll`**：去掉了上限，但每次调用仍要传入整个数组、内核仍线性扫描，复杂度 O(连接总数)。
- **`epoll`（Linux）和 `kqueue`（macOS/BSD）**：fd 只**注册一次**，内核维护一个就绪列表，调用只返回就绪的，复杂度 O(就绪数)。

实测（macOS，Python，N 个空闲连接里只有 1 个就绪，每次 `poll`/`kqueue` 调用的耗时）：
| 连接数 N | `poll` | `kqueue` |
|---|---|---|
| 100 | 约 14 微秒 | 约 0.4 微秒 |
| 1000 | 约 120 微秒 | 约 0.3 微秒 |
| 10000 | 约 1150 微秒 | 约 0.3 微秒 |

`poll` 随连接数线性增长，1 万连接时一次调用 1 毫秒多，事件循环每轮都要付；`kqueue` 与连接总数无关。这就是 C10K 问题被解决的技术核心：**把成本从“连接总数”改成“活跃连接数”**。

有一个常见误解：这些接口只告诉你“可读”，不替你读。就绪之后你仍要自己调用 `read`，所以每个事件至少两次系统调用（等待一次，读一次）。

对应关系：Go 的 netpoller、Java 的 `Selector`、Rust 的 mio/tokio、Python 的 `selectors`/asyncio 在 Linux 上都是 `epoll`，macOS/BSD 上是 `kqueue`，Windows 上运行时通常改用 IOCP（完成通知）。
