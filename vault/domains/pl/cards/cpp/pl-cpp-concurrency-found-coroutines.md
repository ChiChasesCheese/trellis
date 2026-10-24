---
id: pl-cpp-concurrency-found-coroutines
node: cpp.concurrency
type: qa
step: 6
---
## Q
C++20 协程（coroutine）是什么？"无栈"协程怎样工作，为什么说它只提供了机制而没有提供库？

## A
**协程**是可以**暂停并稍后恢复**的函数。函数里出现 `co_await`（等待一个结果）、`co_yield`（产出一个值并暂停）或 `co_return`，它就成为协程。用途：惰性生成器、异步 I/O（等网络时让出线程）、状态机。

**无栈（stackless）的含义**：协程暂停时，不保留一整条调用栈，只保存**它自己的局部变量和当前执行位置**。编译器把协程函数改写成一个状态机，状态存在一块**协程帧**（coroutine frame）里。

**对比有栈协程**：Go 的 goroutine 有自己的栈（可增长），可以在任意深度的调用里暂停；C++ 协程只能在**协程函数本身**里暂停，调用的普通函数不能让出。好处是帧很小、便宜；代价是"染色"：想在调用链里暂停，整条链都要是协程。

**C++ 只给了钩子**：编译器要求你定义一个返回类型，里面有 `promise_type`，规定协程怎样开始、暂停、产出值、结束。一个最小的生成器：

```cpp
struct Gen { struct promise_type {
  int value;
  Gen get_return_object() { return Gen{std::coroutine_handle<promise_type>::from_promise(*this)}; }
  std::suspend_always initial_suspend() { return {}; }
  std::suspend_always final_suspend() noexcept { return {}; }
  std::suspend_always yield_value(int v) { value = v; return {}; }
  void return_void() {}  void unhandled_exception() { std::terminate(); }
}; /* handle、resume、析构省略 */ };
Gen count_to(int n) { for (int i = 1; i <= n; ++i) co_yield i; }
```

调用 `count_to(3)` 时函数体**一行也不运行**（`initial_suspend` 返回 `suspend_always`）；每次 `resume()` 才跑到下一个 `co_yield`。实测依次得到 1、2、3。

**帧在哪里**：默认在堆上分配。本机实测 `-O0` 下创建协程发生 **1 次堆分配**；`-O2` 下是 0 次，因为编译器发现协程的生命周期被完全包含在调用者里，把帧优化到了栈上（HALO 优化），但这不是保证。

**为什么说只有机制**：写一个能用的 `Task`、`Generator` 要手写上面这堆样板。C++23 加入了 `std::generator`（本机的 libc++ 还没有 `<generator>`）；异步任务和调度要等 C++26 的 `std::execution`。生产里大多用第三方库（cppcoro、Boost.Asio、folly、libunifex）。

**与其他语言对比**：Python 的 `async`/`await` 与生成器、Rust 的 `async fn`、JavaScript 的 `async` 同属无栈协程，但它们的运行时（事件循环、`Future` trait）是语言或标准库的一部分；Go 的 goroutine 是有栈的，且调度器内置。

**要记住的一点**：C++20 协程给的是编译器变换，不是并发运行时；直接使用要写大量样板，实际工作靠库。
