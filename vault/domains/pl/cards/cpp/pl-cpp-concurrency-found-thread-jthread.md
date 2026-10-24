---
id: pl-cpp-concurrency-found-thread-jthread
node: cpp.concurrency
type: qa
step: 2
---
## Q
`std::thread` 是什么？为什么忘记 `join` 会让程序终止，`std::jthread`（C++20）怎样改进？

## A
**`std::thread`**：创建一个**操作系统线程**，并立即在其中运行传入的可调用对象（函数、lambda）。它是 1:1 映射：一个 `std::thread` 对应一个内核线程，由操作系统调度，每个线程有独立的栈。本机实测创建加 `join` 一个空线程约 15 μs，比一次函数调用贵几个数量级，所以不适合"每个任务一个线程"。

**生命周期规则**：一个 `std::thread` 对象在销毁时，如果线程还"可汇合"（joinable，即既没有 `join()` 也没有 `detach()`），析构函数调用 `std::terminate`。

```cpp
std::thread t([]{ println("working"); });
// 忘记 t.join()，main 结束，t 被销毁
```

真实输出：`libc++abi: terminating`。为什么这样设计：委员会认为静默 `join`（可能阻塞很久）和静默 `detach`（线程可能访问已销毁的数据）都不安全，所以选择"让违规立刻暴露"。

**`std::jthread`（C++20）**：
1. 析构时自动 `request_stop()` 再 `join()`，符合 RAII；
2. 内置**协作式取消**：线程函数可以接收 `std::stop_token`，循环里查 `stop_requested()`。

```cpp
{ std::jthread worker([&](std::stop_token st) {
    while (!st.stop_requested()) { /* 干活 */ }
    println("worker saw stop request"); });
  sleep_for(20ms); }   // 离开作用域：请求停止并等待结束
```

实测输出 `worker saw stop request`，随后 `joined automatically`。

**`detach()`**：让线程独立运行，没有人等它。危险在于线程可能访问已销毁的栈变量或全局对象。除非有明确的生命周期管理，不要用。

**对比**：Go 的 goroutine 启动成本约 1 μs 量级、栈从 2 KB 起，由运行时调度，不需要 `join`；Java 的平台线程也是 1:1，虚拟线程才是轻量的；Rust 的 `std::thread` 与 C++ 同类，但 `JoinHandle` 被丢弃时线程自动 detach，而且借用检查器阻止它访问局部变量。

**要记住的一点**：C++ 里默认用 `std::jthread`；`std::thread` 只在需要兼容旧标准时用。
