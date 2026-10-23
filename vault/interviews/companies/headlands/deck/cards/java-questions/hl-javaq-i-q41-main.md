---
id: hl-javaq-i-q41-main
node: java-questions.i-network
type: qa
step: 5
---
## Q
阻塞 I/O、NIO、epoll、Netty、虚拟线程：怎么服务大量连接？`read()` 在内核里做什么？
Blocking I/O vs NIO vs epoll vs Netty vs virtual threads: how do you serve many connections? What does `read()` do inside the kernel?

## A
三种模型：
1. **每连接一线程 + 阻塞 I/O**：简单，线程数受限。
2. **反应器**（reactor）：少量线程用 `Selector`（Linux 下是 `epoll`）监听就绪事件，非阻塞读写（Netty 的模型）。
3. **虚拟线程**：写回阻塞风格的代码，JVM 在底层用非阻塞 I/O 调度。

- `select / poll` 每次扫描所有 fd（O(n)）；`epoll` 只返回就绪的（O(就绪数)）。
- **阻塞 `read(fd)`**：线程进内核 → 数据没到 → 线程睡眠（让出 CPU）→ 数据到达中断 → 内核拷贝到用户 buffer → 线程被唤醒。
- **epoll**：`epoll_ctl` 注册 fd 集合；`epoll_wait` 睡到有 fd 就绪，返回就绪列表，再对每个就绪 fd 做非阻塞 `read`。
- Java NIO：`Selector.select()` ≈ `epoll_wait`（Linux）/ `kqueue`（macOS）。
- `C10K` 问题的答案就是 epoll + 非阻塞。
