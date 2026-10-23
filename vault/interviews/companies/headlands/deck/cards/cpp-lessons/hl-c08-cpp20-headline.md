---
id: hl-c08-cpp20-headline
node: cpp-lessons.c08-cxx-standards-tour
type: qa
step: 10
---
## Q
面试问：C++20 你觉得最重要的是什么？四大特性各解决什么痛点？
Interview question: What are the most important C++20 features?

## A
- **Concepts**：给模板参数写约束，错误信息可读（`template <std::integral T>`）。
- **Ranges + views**：惰性管线、投影，取代迭代器对的样板。
- **协程**（`co_await`/`co_yield`/`co_return`）：生成器、异步 I/O 的状态机由编译器生成。
- **Modules**：取代 `#include` 头文件模型，编译更快（单文件面试用不到）。
- 另有：三路比较 `<=>`；`consteval`/`constinit`；`constexpr` 里用 `vector`/`string`。
- 一句话说明各自解决的痛点即可。
