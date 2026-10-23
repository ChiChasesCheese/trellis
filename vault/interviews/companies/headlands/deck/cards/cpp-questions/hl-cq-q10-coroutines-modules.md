---
id: hl-cq-q10-coroutines-modules
node: cpp-questions.b-standards
type: qa
step: 27
---
## Q
C++20 的 concepts、coroutines 和 modules 各解决什么问题？

## A
- **concepts**：价值体现在**错误信息**上，约束不满足时在调用处报清楚的原因。
- **coroutines**：可挂起的函数，用 `co_await` / `co_yield`，用于异步 I/O 和生成器。
- **modules**：用 `import` 取代 `#include`，缓解 `<iostream>` 展开约 8 万行的编译负担。
- 面试里分清哪些你写过、哪些只了解概念，并如实说。
