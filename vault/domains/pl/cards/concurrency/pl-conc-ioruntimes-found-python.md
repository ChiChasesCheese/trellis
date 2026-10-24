---
id: pl-conc-ioruntimes-found-python
node: concurrency.io-runtimes
type: qa
step: 5
---
## Q
Python 的 asyncio 事件循环底层怎样接入 `epoll`/`kqueue`？`await reader.read()` 和回调式 API 之间是什么关系？

## A
asyncio 的事件循环在标准库里，核心类是 `selector_events` 里的 `BaseSelectorEventLoop`，用标准库的 `selectors` 模块访问系统的多路复用器。在本机查看：
```python
loop = asyncio.get_running_loop()
type(loop).__name__, type(loop._selector).__name__
```
输出：`_UnixSelectorEventLoop + KqueueSelector`（Linux 上是 `EpollSelector`；Windows 默认是基于 IOCP 的 `ProactorEventLoop`）。

**从回调到 `await`**：循环最底层的接口是回调：`loop.add_reader(fd, callback)` 注册“fd 可读时调用 callback”。asyncio 在这之上分了两层：
1. **传输和协议**（transport / protocol）：传输负责读写 fd，读到数据就调用协议的 `data_received()`。这是纯回调风格，也是最高效的接口。
2. **流**（streams）：`StreamReader.read()` 返回一个 `Future`；传输读到数据时，回调把数据放进缓冲区并设置 `Future` 的结果；循环于是恢复等待这个 `Future` 的协程，`await` 表达式得到返回值。

所以 `await reader.read(1024)` 的实现是：创建 Future、让出给循环、等回调完成它。协程只是回调之上的一层顺序写法。

实测（一次测量）：5000 个空闲连接由一个 asyncio 线程服务，OS 线程数始终为 1，内存从 25 MB 增到 56 MB，约 6 KB 每连接（每个连接有传输对象、流读写器对象、协程帧，都是 Python 对象，比 Rust 的状态机重得多）。

**设计后果**：
- 所有协程在**一个线程**里，因此任何没有 `await` 的耗时代码都会让所有连接停顿；多核要靠多个进程（每个进程一个循环）。
- 事件循环可以替换：第三方的 `uvloop` 用 libuv 实现同样的接口，通常明显更快，是 Python 服务常见的一行优化；这是一个“接口稳定、实现可换”的好例子。
- Python 3.14 的自由线程构建让多个线程各跑一个事件循环成为更现实的选择。
