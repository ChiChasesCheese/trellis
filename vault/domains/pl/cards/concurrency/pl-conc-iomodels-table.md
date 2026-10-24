---
id: pl-conc-iomodels-table
node: concurrency.io-models
type: qa
step: 6
---
## Q
Go、Java、Rust、Python、C++ 的标准库分别默认提供哪种 I/O 模型？为什么语言设计者在“一连接一线程”和“事件循环”之间的选择不同？

## A
| 语言 | 默认暴露给程序员的模型 | 底层实际的模型 | 换来 | 代价 |
|---|---|---|---|---|
| Go | 阻塞风格（`conn.Read`） | 非阻塞 fd + 运行时内置的 epoll/kqueue 轮询器 | 代码顺序易读，上万 goroutine 无压力 | 隐藏了调度与内存成本，阻塞型系统调用需要运行时特殊处理 |
| Java | 经典 `java.io` 阻塞；`NIO` 的 `Selector`（就绪）；JDK 21 起虚拟线程 | 平台线程阻塞，或 Selector + epoll；虚拟线程由 JDK 内部轮询线程唤醒 | 三代 API 共存，生态最大（Netty 做事件驱动，Tomcat 现在可用虚拟线程） | 历史包袱重，要选对 API |
| Rust | 标准库只有阻塞；异步靠 `Future` + 第三方运行时（tokio、async-std） | mio 封装 epoll/kqueue/IOCP，tokio 在其上调度任务 | 零成本、可控，状态机很小 | 需要选运行时；`async` 的函数着色、取消语义复杂 |
| Python | 阻塞 socket；`asyncio` 事件循环 | `selectors`（epoll/kqueue）；Windows 默认 IOCP | 一个线程撑上万并发；标准库自带 | 单线程跑 Python 代码，不 `await` 的耗时操作会卡住所有任务 |
| C++ | 标准库没有网络和事件循环，只有阻塞的 iostream；实际用系统调用或 Boost.Asio（事实标准，完成模型的封装） | Asio 在 Windows 用 IOCP，Linux 用 epoll（可选 io_uring） | 想要哪个模型就拿哪个，没有隐含成本 | 没有默认答案，每个项目自己选库；Asio 学习曲线陡 |

**设计者逻辑**：
- **Go** 的目标是让写服务的人不必意识到事件循环的存在，所以把轮询器放进运行时，向外只留阻塞语义。
- **Java** 在 1990 年代就有了线程，生态已经围绕阻塞 API 建立；NIO 是后补的性能出路，虚拟线程则是为了让旧的阻塞代码也能扛高并发。
- **Rust** 不想要运行时的隐含成本，所以语言只给 `async/await` 语法，把“谁来驱动”留给库，用户为此多做一次选择。
- **Python** 有 GIL，线程无法并行，I/O 并发本来就适合事件循环，所以 `asyncio` 进了标准库。
- **C++** 的标准库只描述语言和算法，不碰操作系统接口：网络库（Networking TS）始终没有进入标准，I/O 模型留给平台和第三方。这是 C 兼容和零开销的延伸：语言不替你选 I/O 模型，也就没有什么要为不用的模型付费。

本质区别：**“阻塞”是编程模型，不是执行模型**。Go 和 Java 虚拟线程展示了前者可以与后者脱钩：写阻塞代码，实际跑事件循环。
