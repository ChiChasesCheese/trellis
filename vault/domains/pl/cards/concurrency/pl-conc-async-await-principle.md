---
id: pl-conc-async-await-principle
node: concurrency.async-await
type: qa
step: 1
---
## Q
`async/await` 是什么？它要解决什么问题，什么叫「函数着色」（function coloring）问题？

## A
**问题**：一个线程阻塞等 I/O 时什么也做不了，要同时处理上万个连接就要上万个线程。另一条路是让**一个线程**同时盯着很多个连接：用事件循环（event loop）调用 `epoll`/`kqueue` 等待「哪些连接就绪了」，就绪的再执行。早期写法是回调，逻辑被切成碎片（回调地狱）；后来是 Promise/Future 链式调用；`async/await` 让你**把异步代码写得像顺序代码**。

**机制**：
- 用 `async` 声明的函数调用后不会执行函数体，只返回一个代表「将来的结果」的对象（Rust 的 `Future`、Python 的协程对象）。
- 在 `async` 函数里写 `await x`，意思是：如果 `x` 还没好，就把我挂起，让事件循环去跑别的任务；`x` 好了再从这里继续。
- 切换只发生在 `await` 处，属于**协作式**（cooperative）调度，不需要线程。

**函数着色**：`await` 只能写在 `async` 函数里，所以函数分成两种「颜色」：同步的和异步的。
- 同步函数不能直接 `await`，也拿不到异步函数的结果。
- 一旦一个底层函数变成 `async`，所有调用它的函数都要跟着变，颜色沿调用链向上传染；库也要同步、异步各写一套。

设计空间有三种：回调 / Future 链；async/await（有颜色）；让阻塞调用本身便宜（goroutine、虚拟线程，没有颜色）。
