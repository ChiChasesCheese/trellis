---
id: pl-conc-async-await-found-asyncio
node: concurrency.async-await
type: qa
step: 2
---
## Q
Python 的 `async def`、`await`、协程对象、事件循环（event loop）和 `asyncio.gather` 各是什么？
请用三个会“等待”的任务说明执行顺序。

## A
- **`async def` 函数**：调用它**不会执行函数体**，而是返回一个**协程对象**（coroutine object），像一个“尚未启动的任务说明书”。
- **`await 表达式`**：只能写在 `async def` 里。含义是：“这件事还要等一会儿，我先暂停，让事件循环去跑别的；好了再叫我，我从这里继续。”
- **事件循环**：一个调度器，反复做“取出一个能继续跑的协程，运行到它下一个 `await`，再取下一个”。所有协程都在同一个线程里，一次只有一个在运行。
- **`asyncio.sleep(d)`**：一个“等 d 秒”的可 `await` 对象（不占线程）。
- **`asyncio.gather(a, b, c)`**：把几个协程都交给事件循环并发运行，等全部完成，按传入顺序返回结果。

```python
async def fetch(name, delay):
    print(f"{name} start")
    await asyncio.sleep(delay)         # suspend here; the loop runs others
    print(f"{name} done")
    return name

async def main():
    results = await asyncio.gather(fetch("A", 0.3), fetch("B", 0.1), fetch("C", 0.2))
    print(results)
asyncio.run(main())
```
输出：
```
A start
B start
C start
B done
C done
A done
['A', 'B', 'C']
```
读法：`A`、`B`、`C` 依次启动，每个都在 `await` 处把控制权交还事件循环，所以三个“开始”紧挨着打印；谁等待的时间短谁先完成（B 0.1 秒、C 0.2 秒、A 0.3 秒）；总耗时约 0.3 秒而不是 0.6 秒；返回值的顺序仍是传入顺序。整个过程只用一个线程。

`asyncio.run(main())` 是进入异步世界的入口：创建事件循环、运行 `main`、结束后关闭。
