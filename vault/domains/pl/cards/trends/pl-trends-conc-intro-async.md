---
id: pl-trends-conc-intro-async
node: trends.concurrency-evolution
type: qa
step: 3
---
## Q
`async`/`await` 是什么？事件循环和“函数染色”（function coloring）分别指什么，一个例子里它怎样工作？

## A
**是什么**：`async` 函数调用后不立即执行，而返回一个代表“未完成的计算”的对象（Python 的协程、JavaScript 的 Promise、Rust 的 `Future`）。`await` 表示“这里要等一个结果，把线程让给别人”。编译器把函数改写成**状态机**，每个 `await` 是一个暂停点。

**事件循环**（event loop）：一个线程反复做：取出一个就绪的任务，运行到下一个 `await` 为止，再换下一个。等待 I/O 的任务被登记到操作系统的就绪通知机制（epoll、kqueue），就绪后重新排队。一个线程就能同时驱动成千上万个等待中的任务。

**函数染色**：`async` 函数只能在 `async` 函数里用 `await` 调用，普通函数调用它拿到的只是个未执行的对象。于是函数被分成两种“颜色”，异步性会沿着调用链向上传染，一个库如果提供了同步和异步两套 API，就要写两份。

```python
async def good(): await asyncio.sleep(1)
async def bad():  time.sleep(1)       # blocks the whole loop
```

三个任务并发运行：用 `asyncio.sleep` 总共 **1.0 秒**，用阻塞的 `time.sleep` 总共 **3.4 秒**（真实输出），因为 `time.sleep` 占着唯一的线程，其他任务无法运行。

**Rust 的 async 有特别之处**：`Future` 本身是惰性的状态机，语言不带运行时，需要选一个库（tokio、async-std）来驱动它，并且没有垃圾回收，因此借用和生命周期在异步里更复杂。

**要记住的一点**：async 的优势是极低的单任务成本和精确的切换点；代价是染色以及“不能在 async 里阻塞”的纪律。
