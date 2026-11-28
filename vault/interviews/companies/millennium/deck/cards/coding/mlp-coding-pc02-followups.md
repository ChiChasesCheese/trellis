---
id: mlp-coding-pc02-followups
node: coding.pc02
step: 2
type: qa
---
## Q
**异步分页拉取：追问与变体**｜编程轮

写完并发分页拉取后，面试官会追问 asyncio 的原理，或者让你排查"输出丢了"。常见的追问有哪些？

## A
- **协程和线程的区别：** 协程在单线程里协作式调度，靠 `await` 主动让出控制权；线程由操作系统抢占式切换。asyncio 的并发来自"等 I/O 时让出"，不靠多核。
- **事件循环（event loop）在哪：** `asyncio.run()` 创建并驱动事件循环；每个 `await` 都是循环调度别的协程的机会，`gather` 把多个协程交给同一个循环交替推进。
- **"输出丢了"的典型 bug：** 在每个任务里直接往共享列表 `append`，顺序变成谁先返回谁在前，看起来像数据错位或丢失。修法：按页码下标写入预留的位置。
- **漏写 `await` 会怎样：** 拿到的是协程对象而不是结果，后面对它 `extend` 或取下标会报类型错误，或者悄悄拿到空值，排查比直接崩溃更麻烦。
- **重试里用同步 `time.sleep`：** 会卡住整个事件循环，其他协程一起停摆；必须 `await asyncio.sleep`。
- **加超时：** 用 `asyncio.wait_for` 包住调用，超时转成临时错误，复用同一套重试逻辑：

```python
try:
    return await asyncio.wait_for(fetch_page(page), timeout=2.0)
except asyncio.TimeoutError:
    raise TransientError()
```

- **会多花一个测试用例的边界：** 某页为空（不能让后面的页错位）；只有 1 页（不需要并发）；`max_concurrency < 1` 抛 `ValueError`；非临时异常不重试，也不该调用 sleep；失败次数刚好等于 `max_retries` 仍应成功，多一次就把错误抛出来；不同页有重复条目时按首次出现保留一份。

**英文答法。**
- "A coroutine is **cooperative** and single-threaded: it yields at every `await`."
- "The missing output was an **ordering** bug, not lost data: tasks appended in completion order."
- "I only retry **transient** errors, and I use `asyncio.sleep` so I don't block the **event loop**."
