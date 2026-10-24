---
id: pl-conc-async-await-found-rust-future
node: concurrency.async-await
type: qa
step: 3
---
## Q
Rust 的 `async fn` 和 `Future` 是什么？`poll`、`Pending`、`Waker` 各是什么，一个 `Future` 在内存里多大？

## A
Rust 的 `async fn` 被编译成一个**状态机**（state machine）：一个枚举类型，每个 `await` 点是一个状态，跨 `await` 仍然要用的局部变量存在这个枚举里。它实现了 `Future` trait：

`fn poll(self: Pin<&mut Self>, cx: &mut Context) -> Poll<Output>`

- 执行器（executor）调用 `poll`，状态机运行到下一个 `await`。
- 返回 `Poll::Ready(v)`：任务完成。
- 返回 `Poll::Pending`：还没好，同时登记 `cx.waker()`（唤醒器）；等 I/O 就绪或定时器到期时，来源调用 `waker.wake()`，执行器就再次 `poll` 它。

一个手写的小例子（自定义的 `YieldOnce` 第一次返回 `Pending`），`job` 里有两个 `await`：
```
created, nothing printed yet; size = 2 bytes
step 1
pending
step 2
pending
step 3
ready(7) after 3 polls
```
创建 `job()` 时没有任何输出，因为什么也没执行；3 次 `poll` 才跑完。大小只有 2 字节（两个 `YieldOnce` 的状态位）；如果在 `await` 之前定义了 `[0u8; 1000]` 并在之后使用，future 就变成 1002 字节。

结论：Rust 的异步任务没有独立的栈，大小就是状态机本身，可以非常小，几十万个任务也很轻，代价是编译器要重写函数，并且必须有执行器反复 `poll`。Python 的协程则是保存着帧（frame）的对象，由事件循环用 `send()` 驱动。

补充：Rust 标准库只定义了 `Future` 和 `async/await` 语法，**不带执行器**。真正驱动 `poll` 的执行器、定时器和网络轮询由第三方运行时提供，最常用的是 tokio（用 `#[tokio::main]` 启动、`tokio::spawn` 提交任务）。Python 则把这些内置在标准库的 `asyncio` 里。
