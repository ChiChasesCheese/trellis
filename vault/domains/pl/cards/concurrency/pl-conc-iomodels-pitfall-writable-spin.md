---
id: pl-conc-iomodels-pitfall-writable-spin
node: concurrency.io-models
type: qa
step: 9
---
## Q
事件循环里订阅了“可写”事件却没有数据要写，为什么会让 CPU 打满？电平触发模型下，这类 bug 的特征是什么？

## A
对一个连接，“可读”表示接收缓冲区里有数据；“可写”表示发送缓冲区还有空间。大部分时间里，**发送缓冲区都有空位**，所以“可写”几乎永远是真。在电平触发模型下，只要条件为真，每次询问都会立刻返回这个事件。

实测（Python，`selectors`，macOS 上是 `KqueueSelector`）：把一个空闲连接同时注册为可读和可写，然后循环 `select`：
```python
sel.register(a, selectors.EVENT_READ | selectors.EVENT_WRITE)
while time.perf_counter() < end:
    for key, ev in sel.select(timeout=1):
        wakeups += 1          # nothing to read, nothing to write
```
输出：`wakeups in 100 ms: 221045 cpu ms: 100`。100 毫秒内醒了 22 万次，CPU 时间也是 100 毫秒（占满一个核）；改成只订阅 `EVENT_READ` 后，同样 `select(timeout=0.1)` 等了 102 毫秒，CPU 时间约 0。

**症状**：一个本该空闲的服务进程 CPU 100%，`strace`/`dtruss` 里全是连续的 `epoll_wait` 立刻返回；延迟反而变高，因为事件循环忙于处理无意义的事件。

**正确做法**：只在**有数据要写而且上一次没写完**（`send` 返回了部分字节或 `EAGAIN`）时才订阅可写事件，写完立刻取消。这就是成熟的框架里“写缓冲区”的逻辑：
1. 先直接尝试 `send`；
2. 没写完才把剩余数据放进缓冲区并订阅可写；
3. 缓冲区排空后取消订阅。

**相关的另一类事故**是慢客户端：缓冲区堆积在服务器内存里，一个只读不收的客户端可以拖垮内存；需要缓冲上限和超时。

Go、tokio、asyncio 的用户一般碰不到这个 bug，因为运行时内部已经管理了订阅，除非你直接使用底层的 `selectors`、`mio` 或 `epoll` 接口。
