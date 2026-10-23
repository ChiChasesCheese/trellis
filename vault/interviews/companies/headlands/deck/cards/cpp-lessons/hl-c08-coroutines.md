---
id: hl-c08-coroutines
node: cpp-lessons.c08-cxx-standards-tour
type: qa
step: 13
---
## Q
面试问：C++20 协程（coroutine）是怎么回事？标准库提供了什么，缺了什么？
Interview question: How do C++20 coroutines work, and what does the standard library provide?

## A
- 编译器把含 `co_yield` / `co_await` / `co_return` 的函数变成**可挂起、可恢复的状态机**。
- 标准只提供**机制**：`std::coroutine_handle`、`suspend_always`、`promise_type`；**不提供**现成的 generator/task 类型（`std::generator` 在 C++23）。
- 所以要自己写 `Generator<T>` 包装 promise 与 handle，然后：

```cpp
Generator<int> fibs() {
    int a = 0, b = 1;
    for (;;) { co_yield a; int t = a + b; a = b; b = t; }
}
// 依次得到 0 1 1 2 3 5 8 13 21 34
```
- 性能：协程帧可能堆分配。
